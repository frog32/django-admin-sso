try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
from django.utils import unittest

from admin_sso import settings
from admin_sso.auth import DjangoSSOAuthBackend
from admin_sso.models import Assignment

SREG_NS = "http://openid.net/sreg/1.0"


class AuthModuleTests(unittest.TestCase):
    def setUp(self):
        self.auth_module = DjangoSSOAuthBackend()
        self.user1 = User.objects.create(username='admin_sso1')
        self.user2 = User.objects.create(username='admin_sso2')
        self.user3 = User.objects.create(username='admin_sso3')
        self.assginment1 = Assignment.objects.create(username='',
                                                     username_mode=settings.ASSIGNMENT_ANY,
                                                     domain='example.com',
                                                     user=self.user1,
                                                     weight=100)
        self.assginment2 = Assignment.objects.create(username='*bar',
                                                     username_mode=settings.ASSIGNMENT_MATCH,
                                                     domain='example.com',
                                                     user=self.user2,
                                                     weight=200)
        self.assginment3 = Assignment.objects.create(username='foo*',
                                                     username_mode=settings.ASSIGNMENT_EXCEPT,
                                                     domain='example.com',
                                                     user=self.user3,
                                                     weight=300)

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()
        Assignment.objects.all().delete()

    def test_domain_matches(self):
        email = "foo@example.com"
        user = self.auth_module.authenticate(sso_email=email)
        self.assertEquals(user, self.user1)

    def test_invalid_domain(self):
        email = 'someone@someotherdomain.com'
        user = self.auth_module.authenticate(sso_email=email)
        self.assertIsNone(user)

    def test_domain_matches_and_username_ends_with_bar(self):
        email = "foobar@example.com"
        user = self.auth_module.authenticate(sso_email=email)
        self.assertEquals(user, self.user2)

    def test_domain_matches_and_username_doesnt_begin_with_foo(self):
        email = "bar@example.com"
        user = self.auth_module.authenticate(sso_email=email)
        self.assertEquals(user, self.user3)

    def test_invalid_email(self):
        email = 'invalid'
        user = self.auth_module.authenticate(sso_email=email)
        self.assertEquals(user, None)

    def test_no_sso_email_param(self):
        user = self.auth_module.authenticate()
        self.assertEquals(user, None)

    def test_change_weight(self):
        self.assginment2.weight = 50
        self.assginment2.save()
        email = "foobar@example.com"
        user = self.auth_module.authenticate(sso_email=email)
        self.assertEquals(user, self.user1)
