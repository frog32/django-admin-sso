from django.utils import unittest
from django.contrib.auth.models import User

from openid.consumer.consumer import SuccessResponse
from openid.consumer.discover import OpenIDServiceEndpoint
from openid.message import Message, OPENID2_NS

from django_admin_sso import settings
from django_admin_sso.auth import DjangoSSOAuthBackend
from django_admin_sso.models import Assignment, OpenIDUser

SREG_NS = "http://openid.net/sreg/1.0"


class AuthModuleTests(unittest.TestCase):
    def setUp(self):
        self.auth_module = DjangoSSOAuthBackend()
        self.user1 = User.objects.create(username='django_admin_sso1')
        self.user2 = User.objects.create(username='django_admin_sso2')
        self.user3 = User.objects.create(username='django_admin_sso3')
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
        OpenIDUser.objects.all().delete()

    def test_domain_matches(self):
        response = self.create_sreg_response(fullname="User Name", email="foo@example.com", identifier='7324')
        user = self.auth_module.authenticate(openid_response=response)
        self.assertEquals(user, self.user1)

    def test_invalid_domain(self):
        response = self.create_sreg_response(email='someone@someotherdomain.com')
        user = self.auth_module.authenticate(openid_response=response)
        self.assertIsNone(user)

    def test_domain_matches_and_username_ends_with_bar(self):
        response = self.create_sreg_response(fullname="User Name", email="foobar@example.com", identifier='5673')
        user = self.auth_module.authenticate(openid_response=response)
        self.assertEquals(user, self.user2)

    def test_login_twice_and_reuse_stored_openid(self):
        response = self.create_sreg_response(fullname="User Name", email="foobar@example.com", identifier='1111')
        user = self.auth_module.authenticate(openid_response=response)
        self.assertEquals(user, self.user2)
        response = self.create_sreg_response(identifier='1111')
        user = self.auth_module.authenticate(openid_response=response)
        self.assertEquals(user, self.user2)

    def test_domain_matches_and_username_doesnt_begin_with_foo(self):
        response = self.create_sreg_response(fullname="User Name", email="bar@example.com", identifier='3476')
        user = self.auth_module.authenticate(openid_response=response)
        self.assertEquals(user, self.user3)

    def test_change_weight(self):
        self.assginment2.weight = 50
        self.assginment2.save()
        response = self.create_sreg_response(fullname="User Name", email="foobar@example.com", identifier='5673')
        user = self.auth_module.authenticate(openid_response=response)
        self.assertEquals(user, self.user1)

    def create_sreg_response(self, fullname='', email='', identifier=''):
        message = Message(OPENID2_NS)
        message.setArg(SREG_NS, "fullname", fullname)
        message.setArg(SREG_NS, "email", email)
        endpoint = OpenIDServiceEndpoint()
        endpoint.display_identifier = identifier
        return SuccessResponse(endpoint, message, signed_fields=message.toPostArgs().keys())
