from django.db import models
from django.utils.translation import ugettext_lazy as _
try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now

from admin_sso import settings


class Assignment(models.Model):
    username_mode = models.IntegerField(choices=settings.ASSIGNMENT_CHOICES)
    username = models.CharField(max_length=255, blank=True)
    domain = models.CharField(max_length=255)
    copy = models.BooleanField(default=False)
    weight = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('auth.User', null=True, blank=True)

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')
        ordering = ('-weight',)

    def __unicode__(self):
        return u"%s(%s) @%s" % (dict(settings.ASSIGNMENT_CHOICES)[self.username_mode], self.username, self.domain)


class OpenIDUser(models.Model):
    claimed_id = models.TextField(max_length=2047)
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User')
    last_login = models.DateTimeField(_('last login'), default=now)

    class Meta:
        verbose_name = _('OpenIDUser')
        verbose_name_plural = _('OpenIDUsers')

    def __unicode__(self):
        return self.claimed_id

    def update_last_login(self):
        self.last_login = now()
        self.save()


class Nonce(models.Model):
    server_url = models.CharField(max_length=2047)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)


class Association(models.Model):
    server_url = models.CharField(max_length=2047)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)
