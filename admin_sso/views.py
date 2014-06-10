from django.contrib.sites.models import RequestSite
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from oauth2client.client import OAuth2WebServerFlow

from admin_sso import settings


flow = OAuth2WebServerFlow(client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
                           client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
                           scope='email',
                           redirect_uri='http://127.0.0.1:8000/admin/admin_sso/assignment/end/')


def start(request):
    return HttpResponseRedirect(flow.step1_get_authorize_url())


def end(request):
    # import pdb; pdb.set_trace()
    code = request.GET.get('code', None)
    if not code:
        return HttpResponseRedirect('/')  # this should point somewhere else
    credentials = flow.step2_exchange(code)

    if credentials.id_token['verified_email']:
        email = credentials.id_token['email']
        user = authenticate(sso_email=email)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('admin:index'))

