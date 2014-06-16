from unittest import skipIf

from admin_sso import settings


def skipIfOAuth(test_func):
    """
    Skip a test if a custom user model is in use.
    """
    return skipIf(settings.DJANGO_ADMIN_SSO_USE_OAUTH, 'Using OAuth')(test_func)


def skipIfOpenID(test_func):
    """
    Skip a test if a custom user model is in use.
    """
    return skipIf(not settings.DJANGO_ADMIN_SSO_USE_OAUTH, 'Using OpenID')(test_func)
