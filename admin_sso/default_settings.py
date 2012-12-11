from django.conf import settings
from django.utils.translation import ugettext_lazy as _

ASSIGNMENT_ANY = 0
ASSIGNMENT_MATCH = 1
ASSIGNMENT_EXCEPT = 2
ASSIGNMENT_CHOICES = ((ASSIGNMENT_ANY, _('any')),
                      (ASSIGNMENT_MATCH, _("matches")),
                      (ASSIGNMENT_EXCEPT, _("don't match")))

AX_MAPPING = (('http://schema.openid.net/contact/email', 'email'),
              ('http://schema.openid.net/namePerson', 'fullname'),
              ('http://axschema.org/contact/email', 'email'),
              ('http://axschema.org/namePerson', 'fullname'),
              ('http://axschema.org/namePerson/first', 'firstname'),
              ('http://axschema.org/namePerson/last', 'lastname'))

DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON = getattr(settings, 'DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON', True)

DJANGO_ADMIN_SSO_OPENID_ENDPOINT = getattr(settings, 'DJANGO_ADMIN_SSO_OPENID_ENDPOINT', 'https://www.google.com/accounts/o8/id')

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
