from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_sso import settings

class Assignment(models.Model):
    username_mode = models.IntegerField(choices=settings.ASSIGNMENT_CHOICES)
    username = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    copy = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User')
    
    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')

    def __unicode__(self):
        return u"%s@%s" % (dict(settings.ASSIGNMENT_CHOICES)[self.username_mode], self.domain)


class OpenIDUser(models.Model):
    claimed_id = models.TextField(max_length=2047, unique=True)
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User')
