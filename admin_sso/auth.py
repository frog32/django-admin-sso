import fnmatch

try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from admin_sso import settings
from admin_sso.models import Assignment


class DjangoSSOAuthBackend(object):

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, **kwargs):
        sso_email = kwargs.pop('sso_email', None)

        if not sso_email:
            return None

        try:
            username, domain = sso_email.split('@')
        except ValueError:
            return None
        possible_assignments = Assignment.objects.filter(domain=domain)
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
        return used_assignment.user
