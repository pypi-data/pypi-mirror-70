import logging

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template import loader
from django.urls import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from djangoldp.fields import LDPUrlField
from djangoldp.models import Model
from threading import Thread
from djangoldp_notification.middlewares import MODEL_MODIFICATION_USER_FIELD
from djangoldp_notification.permissions import InboxPermissions, SubscriptionsPermissions


class Notification(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inbox', on_delete=models.deletion.CASCADE)
    author = LDPUrlField()
    object = LDPUrlField()
    type = models.CharField(max_length=255)
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    class Meta(Model.Meta):
        owner_field = 'user'
        ordering = ['-date']
        permission_classes = [InboxPermissions]
        anonymous_perms = ['add']
        authenticated_perms = ['inherit']
        owner_perms = ['view', 'change', 'control']

    def __str__(self):
        return '{}'.format(self.type)

    def save(self, *args, **kwargs):
        # I cannot send a notification to myself
        if self.author.startswith(settings.SITE_URL):
            try:
                # author is a WebID.. convert to local representation
                author = Model.resolve(self.author.replace(settings.SITE_URL, ''))[1]
            except NoReverseMatch:
                author = None
            if author == self.user:
                return

        super(Notification, self).save(*args, **kwargs)


class Subscription(Model):
    object = models.URLField()
    inbox = models.URLField()

    def __str__(self):
        return '{}'.format(self.object)

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ["add", "view", "delete"]
        permission_classes = [SubscriptionsPermissions]

    def save(self, *args, **kwargs):
        # save subscriptions for nested fields
        if self.pk is None and not self.is_backlink and self.object.startswith(settings.SITE_URL):
            try:
                # object is a WebID.. convert to local representation
                local = Model.resolve(self.object.replace(settings.SITE_URL, ''))[0]
                nested_fields = Model.get_meta(local, 'nested_fields', [])

                for nested_field in nested_fields:
                    nested_url = str(self.object) + '1/' + nested_field + '/'

                    # we have the nested_url, but we want the model contained within's container
                    nested_container = Model.resolve(nested_url)[0]
                    nested_container_url = Model.absolute_url(nested_container)

                    # check a Subscription on this pair doesn't exist already
                    existing_subscriptions = Subscription.objects.filter(object=nested_container_url, inbox=self.inbox)
                    # save a Subscription on this container
                    if not existing_subscriptions.exists():
                        Subscription.objects.create(object=nested_container_url, inbox=self.inbox, is_backlink=True)
            except:
                pass

        super(Subscription, self).save(*args, **kwargs)


# --- SUBSCRIPTION SYSTEM ---
@receiver(post_save, dispatch_uid="callback_notif")
@receiver(post_delete, dispatch_uid="delete_callback_notif")
def send_notification(sender, instance, **kwargs):
    if sender != Notification:
        threads = []
        try:
            url_container = settings.BASE_URL + Model.container_id(instance)
            url_resource = settings.BASE_URL + Model.resource_id(instance)
        except NoReverseMatch:
            return

        # dispatch a notification for every Subscription on this resource
        for subscription in Subscription.objects.filter(models.Q(object=url_resource) | models.Q(object=url_container)):
            if not instance.is_backlink:
                process = Thread(target=send_request, args=[subscription.inbox, url_resource, instance,
                                                            kwargs.get("created", False)])
                process.start()
                threads.append(process)


def send_request(target, object_iri, instance, created):
    unknown = str(_("Auteur inconnu"))
    author = getattr(getattr(instance, MODEL_MODIFICATION_USER_FIELD, unknown), "urlid", unknown)
    request_type = "creation" if created else "update"

    try:
        # local inbox
        if target.startswith(settings.SITE_URL):
            user = Model.resolve_parent(target.replace(settings.SITE_URL, ''))
            Notification.objects.create(user=user, object=object_iri, type=request_type, author=author)
        # external inbox
        else:
            json = {
                "@context": settings.LDP_RDF_CONTEXT,
                "object": object_iri,
                "author": author,
                "type": request_type
            }
            requests.post(target, json=json, headers={"Content-Type": "application/ld+json"})
    except Exception as e:
        logging.error('Djangoldp_notifications: Error with request: {}'.format(e))
    return True


@receiver(post_save, sender=Notification)
def send_email_on_notification(sender, instance, created, **kwargs):
    if created and instance.summary and settings.JABBER_DEFAULT_HOST and instance.user.email:
        # get author name, and store in who
        try:
            # local author
            if instance.author.startswith(settings.SITE_URL):
                who = str(Model.resolve_id(instance.author.replace(settings.SITE_URL, '')))
            # external author
            else:
                who = requests.get(instance.author).json()['name']
        except:
            who = "Personne inconnue"

        # get identifier for resource triggering notification, and store in where
        try:
            if instance.object.startswith(settings.SITE_URL):
                where = str(Model.resolve_id(instance.object.replace(settings.SITE_URL, '')))
            else:
                where = requests.get(instance.object).json()['name']
        except:
            where = "Endroit inconnu"

        if who == where:
            where = "t'a envoyé un message privé"
        else:
            where = "t'a mentionné sur " + where

        html_message = loader.render_to_string(
            'email.html',
            {
                'on': (settings.INSTANCE_DEFAULT_CLIENT or settings.JABBER_DEFAULT_HOST),
                'instance': instance,
                'author': who,
                'object': where
            }
        )

        send_mail(
            'Notification sur ' + (settings.INSTANCE_DEFAULT_CLIENT or settings.JABBER_DEFAULT_HOST),
            instance.summary,
            settings.EMAIL_HOST_USER or "noreply@" + settings.JABBER_DEFAULT_HOST,
            [instance.user.email],
            fail_silently=True,
            html_message=html_message
        )
