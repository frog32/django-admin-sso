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
