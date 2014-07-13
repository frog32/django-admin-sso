from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from admin_sso import settings


class OpenIDUser(models.Model):
    claimed_id = models.TextField(max_length=2047)
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    last_login = models.DateTimeField(_('last login'), default=now)

    class Meta:
        verbose_name = _('OpenIDUser')
        verbose_name_plural = _('OpenIDUsers')
        app_label = 'admin_sso'

    def __unicode__(self):
        return self.claimed_id

    def update_last_login(self):
        self.last_login = now()
        self.save()


class Nonce(models.Model):
    server_url = models.CharField(max_length=2047)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    class Meta:
        app_label = 'admin_sso'


class Association(models.Model):
    server_url = models.CharField(max_length=2047)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        app_label = 'admin_sso'
