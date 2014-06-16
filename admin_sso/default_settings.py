import warnings
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# use oauth is set if settings has a client id
DJANGO_ADMIN_SSO_USE_OAUTH = hasattr(settings, 'DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID')

if not DJANGO_ADMIN_SSO_USE_OAUTH:
    warnings.warn(
        "OpenID support is deprecated add DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID and DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET to your settings to use OAuth",
        DeprecationWarning)

ASSIGNMENT_ANY = 0
ASSIGNMENT_MATCH = 1
ASSIGNMENT_EXCEPT = 2
ASSIGNMENT_CHOICES = ((ASSIGNMENT_ANY, _('any')),
                      (ASSIGNMENT_MATCH, _("matches")),
                      (ASSIGNMENT_EXCEPT, _("don't match")))

DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON = getattr(settings, 'DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON', True)

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID = getattr(settings, 'DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID', None)
DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET = getattr(settings, 'DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET', None)

DJANGO_ADMIN_SSO_AUTH_URI = getattr(settings, 'DJANGO_ADMIN_SSO_AUTH_URI', None)
DJANGO_ADMIN_SSO_TOKEN_URI = getattr(settings, 'DJANGO_ADMIN_SSO_TOKEN_URI', None)
DJANGO_ADMIN_SSO_REVOKE_URI = getattr(settings, 'DJANGO_ADMIN_SSO_REVOKE_URI', None)


# settings for deprecated openid part
AX_MAPPING = (('http://schema.openid.net/contact/email', 'email'),
              ('http://schema.openid.net/namePerson', 'fullname'),
              ('http://axschema.org/contact/email', 'email'),
              ('http://axschema.org/namePerson', 'fullname'),
              ('http://axschema.org/namePerson/first', 'firstname'),
              ('http://axschema.org/namePerson/last', 'lastname'))

DJANGO_ADMIN_SSO_OPENID_ENDPOINT = getattr(settings, 'DJANGO_ADMIN_SSO_OPENID_ENDPOINT', 'https://www.google.com/accounts/o8/id')
