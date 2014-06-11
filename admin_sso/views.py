from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError

from admin_sso import settings

flow_kwargs = {
    'client_id': settings.DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID,
    'client_secret': settings.DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET,
    'scope': 'email',
}
if settings.DJANGO_ADMIN_SSO_AUTH_URI:
    flow_kwargs['auth_uri'] = settings.DJANGO_ADMIN_SSO_AUTH_URI

if settings.DJANGO_ADMIN_SSO_TOKEN_URI:
    flow_kwargs['token_uri'] = settings.DJANGO_ADMIN_SSO_TOKEN_URI

if settings.DJANGO_ADMIN_SSO_REVOKE_URI:
    flow_kwargs['revoke_uri'] = settings.DJANGO_ADMIN_SSO_REVOKE_URI

redirect_uri = ''  # set this after end view has been defined

flow_override = None


def start(request):
    flow = OAuth2WebServerFlow(
        redirect_uri=request.build_absolute_uri(redirect_uri),
        **flow_kwargs)

    return HttpResponseRedirect(flow.step1_get_authorize_url())


def end(request):
    if flow_override is None:
        flow = OAuth2WebServerFlow(
            redirect_uri=request.build_absolute_uri(redirect_uri),
            **flow_kwargs)
    else:
        flow = flow_override

    code = request.GET.get('code', None)
    if not code:
        return HttpResponseRedirect(reverse('admin:index'))
    try:
        credentials = flow.step2_exchange(code)
    except FlowExchangeError:
        return HttpResponseRedirect(reverse('admin:index'))

    if credentials.id_token['verified_email']:
        email = credentials.id_token['email']
        user = authenticate(sso_email=email)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('admin:index'))

    # if anything fails redirect to admin:index
    return HttpResponseRedirect(reverse('admin:index'))


redirect_uri = reverse('admin:admin_sso_assignment_end')
