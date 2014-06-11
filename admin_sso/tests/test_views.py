from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from admin_sso.models import Assignment
from admin_sso import settings

try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class CredentialsMock(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class FlowMock(object):
    """
    object to mock a flow and return all arguments given to __init__
    when calling step2_exchange
    """


    def __init__(self, id_token):
        self.credentials = CredentialsMock(id_token=id_token)

    def step2_exchange(self, *args, **kwargs):
        return self.credentials


class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='admin_sso')
        self.assignment = Assignment.objects.create(username='',
                                                    username_mode=settings.ASSIGNMENT_ANY,
                                                    domain='example.com',
                                                    user=self.user,
                                                    weight=100)

    def test_start_view(self):
        start_url = reverse('admin:admin_sso_assignment_start')
        rv = self.client.get(start_url)
        self.assertEqual(rv.status_code, 302)
        self.assertTrue('Location' in rv)
        self.assertTrue(rv['Location'].startswith(settings.DJANGO_ADMIN_SSO_AUTH_URI))

    def test_end_without_code(self):
        end_url = reverse('admin:admin_sso_assignment_end')
        rv = self.client.get(end_url)
        self.assertEqual(rv.status_code, 302)
        self.assertTrue('Location' in rv)
        self.assertTrue(rv['Location'].endswith('/admin/'))

    def test_end_with_invalid_code(self):
        end_url = reverse('admin:admin_sso_assignment_end')
        rv = self.client.get(end_url + '?code=xxx')
        self.assertEqual(rv.status_code, 302)
        self.assertTrue('Location' in rv)
        self.assertTrue(rv['Location'].endswith('/admin/'))

    def test_end_with_sucess(self):
        from admin_sso import views
        setattr(views, 'flow_override', FlowMock({'verified_email': True, 'email': 'test@example.com'}))
        end_url = reverse('admin:admin_sso_assignment_end')
        rv = self.client.get(end_url + '?code=xxx')
        self.assertEqual(rv.status_code, 302)
        self.assertTrue('Location' in rv)
        self.assertEquals(self.client.session['_auth_user_id'], self.user.id)
        self.assertEquals(self.client.session['_auth_user_backend'], 'admin_sso.auth.DjangoSSOAuthBackend')
        setattr(views, 'flow_override', None)

    def test_end_with_email_not_verified(self):
        from admin_sso import views
        setattr(views, 'flow_override', FlowMock({'verified_email': False, 'email': 'test@example.com'}))
        end_url = reverse('admin:admin_sso_assignment_end')
        rv = self.client.get(end_url + '?code=xxx')
        self.assertEqual(rv.status_code, 302)
        self.assertTrue('Location' in rv)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertFalse('_auth_user_backend' in self.client.session)
        setattr(views, 'flow_override', None)
