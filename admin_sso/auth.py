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
        if not settings.DJANGO_ADMIN_SSO_USE_OAUTH:
            from .openid.auth import authenticate as authenticate_openid
            return authenticate_openid(self, **kwargs)

        sso_email = kwargs.pop('sso_email', None)

        assignment = Assignment.objects.for_email(sso_email)
        if assignment is None:
            return None
        return assignment.user
