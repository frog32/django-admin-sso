import fnmatch
from django.db import models
from django.utils.translation import ugettext_lazy as _
try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now

from admin_sso import settings

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class AssignmentManager(models.Manager):
    def for_email(self, email):
        if not email:
            return None

        try:
            username, domain = email.split('@')
        except ValueError:
            return None
        possible_assignments = self.filter(domain=domain)
        used_assignment = None
        for assignment in possible_assignments:
            if assignment.username_mode == settings.ASSIGNMENT_ANY:
                used_assignment = assignment
                break
            elif assignment.username_mode == settings.ASSIGNMENT_MATCH:
                if fnmatch.fnmatch(username, assignment.username):
                    used_assignment = assignment
                    break
            elif assignment.username_mode == settings.ASSIGNMENT_EXCEPT:
                if not fnmatch.fnmatch(username, assignment.username):
                    used_assignment = assignment
                    break
        if used_assignment is None:
            return None
        return used_assignment


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

    objects = AssignmentManager()


if not settings.DJANGO_ADMIN_SSO_USE_OAUTH:
    from .openid.models import OpenIDUser, Association, Nonce  # noqa
