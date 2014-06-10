from django.db import models
from django.utils.translation import ugettext_lazy as _
try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now

from admin_sso import settings

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Assignment(models.Model):
    username_mode = models.IntegerField(choices=settings.ASSIGNMENT_CHOICES)
    username = models.CharField(max_length=255, blank=True)
    domain = models.CharField(max_length=255)
    copy = models.BooleanField(default=False)
    weight = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')
        ordering = ('-weight',)

    def __unicode__(self):
        return u"%s(%s) @%s" % (dict(settings.ASSIGNMENT_CHOICES)[self.username_mode], self.username, self.domain)
