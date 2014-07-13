try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
from django.utils import unittest

from openid.consumer.consumer import SuccessResponse
from openid.consumer.discover import OpenIDServiceEndpoint
from openid.message import Message, OPENID2_NS

from admin_sso import settings
from admin_sso.auth import DjangoSSOAuthBackend
from admin_sso.models import Assignment
from . import skipIfOpenID, skipIfOAuth


SREG_NS = "http://openid.net/sreg/1.0"


class AuthModuleTests(unittest.TestCase):
    def setUp(self):
        self.auth_module = DjangoSSOAuthBackend()
        self.user = User.objects.create(username='admin_sso1')
        self.assignment1 = Assignment.objects.create(username='',
                                                     username_mode=settings.ASSIGNMENT_ANY,
                                                     domain='example.com',
                                                     user=self.user,
                                                     weight=100)

    def tearDown(self):
        self.user.delete()
        Assignment.objects.all().delete()

    def test_empty_authenticate(self):
        user = self.auth_module.authenticate()
        self.assertEqual(user, None)

    @skipIfOpenID
    def test_simple_assignment(self):
        email = "foo@example.com"
        user = self.auth_module.authenticate(sso_email=email)
        self.assertEqual(user, self.user)

    def create_sreg_response(self, fullname='', email='', identifier=''):
        message = Message(OPENID2_NS)
        message.setArg(SREG_NS, "fullname", fullname)
        message.setArg(SREG_NS, "email", email)
        endpoint = OpenIDServiceEndpoint()
        endpoint.display_identifier = identifier
        return SuccessResponse(endpoint, message, signed_fields=message.toPostArgs().keys())

    @skipIfOAuth
    def test_domain_matches(self):
        response = self.create_sreg_response(fullname="User Name", email="foo@example.com", identifier='7324')
        user = self.auth_module.authenticate(openid_response=response)
        self.assertEqual(user, self.user)

    def test_get_user(self):
        user = self.auth_module.get_user(self.user.id)
        self.assertEqual(user, self.user)

        user = self.auth_module.get_user(self.user.id + 42)
        self.assertEqual(user, None)


class AssignmentManagerTests(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin_sso1')
        self.assignment1 = Assignment.objects.create(username='',
                                                     username_mode=settings.ASSIGNMENT_ANY,
                                                     domain='example.com',
                                                     user=self.user,
                                                     weight=100)
        self.assignment2 = Assignment.objects.create(username='*bar',
                                                     username_mode=settings.ASSIGNMENT_MATCH,
                                                     domain='example.com',
                                                     user=self.user,
                                                     weight=200)
        self.assignment3 = Assignment.objects.create(username='foo*',
                                                     username_mode=settings.ASSIGNMENT_EXCEPT,
                                                     domain='example.com',
                                                     user=self.user,
                                                     weight=300)

    def tearDown(self):
        self.user.delete()
        Assignment.objects.all().delete()

    def test_domain_matches(self):
        email = "foo@example.com"
        user = Assignment.objects.for_email(email)
        self.assertEqual(user, self.assignment1)

    def test_invalid_domain(self):
        email = 'someone@someotherdomain.com'
        user = Assignment.objects.for_email(email)
        self.assertIsNone(user)

    def test_domain_matches_and_username_ends_with_bar(self):
        email = "foobar@example.com"
        user = Assignment.objects.for_email(email)
        self.assertEqual(user, self.assignment2)

    def test_domain_matches_and_username_doesnt_begin_with_foo(self):
        email = "bar@example.com"
        user = Assignment.objects.for_email(email)
        self.assertEqual(user, self.assignment3)

    def test_invalid_email(self):
        email = 'invalid'
        user = Assignment.objects.for_email(email)
        self.assertEqual(user, None)

    def test_change_weight(self):
        self.assignment2.weight = 50
        self.assignment2.save()
        email = "foobar@example.com"
        user = Assignment.objects.for_email(email)
        self.assertEqual(user, self.assignment1)
