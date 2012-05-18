from django.contrib.sites.models import RequestSite
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from openid.consumer import consumer
from openid.extensions import ax, pape, sreg
from openid.store.memstore import MemoryStore
from openid.store.filestore import FileOpenIDStore

from django_sso import settings

openid_store = FileOpenIDStore('/tmp/djopenid_c_store')


class OpenIDMixin(object):
    trust_root_url = 'django_sso.root'
    return_to_url = 'django_sso.return'
    
    def get_url(self, url):
        scheme = self.request.is_secure() and 'https' or 'http'
        primary_site = RequestSite(self.request)
        path = reverse(url)
        return '%s://%s%s' % (scheme, primary_site.domain, path)
    
    def get_consumer(self):
        return consumer.Consumer(self.request.session, self.get_openid_store())
    
    def get_openid_store(self):
        return openid_store


class StartOpenIDView(View, OpenIDMixin):
    def get(self, request, *args, **kwargs):
        c = self.get_consumer()
        auth_request = c.begin(settings.DJANGO_SSO_OPENID_ENDPOINT)

        trust_root = self.get_url(self.trust_root_url)
        return_to = self.get_url(self.return_to_url)
        print 'can ax', auth_request.endpoint.supportsType(ax.AXMessage.ns_uri)
        # Add Attribute Exchange request information.
        ax_request = ax.FetchRequest()
        # XXX - uses myOpenID-compatible schema values, which are
        # not those listed at axschema.org.
        for ax_name, field_name in settings.AX_MAPPING:
            ax_request.add(ax.AttrInfo(ax_name, required=True))
        auth_request.addExtension(ax_request)
        
        # sreg_request = sreg.SRegRequest(optional=['email', 'nickname'],
        #                                 required=['dob'])
        # auth_request.addExtension(sreg_request)
        
        if auth_request.shouldSendRedirect():
            url = auth_request.redirectURL(trust_root, return_to)
            return HttpResponseRedirect(url)
        form_id = 'openid_message'
        form_html = auth_request.formMarkup(trust_root, return_to,
                                            False, {'id': form_id})
        return render(
            request, 'django_sso/request_form.html', {'html': form_html})


class FinishOpenIDView(View, OpenIDMixin):
    def get(self, request, *args, **kwargs):
        if request.REQUEST:
            c = self.get_consumer()
            return_to = self.get_url(self.return_to_url)
            response = c.complete(request.REQUEST, return_to)
            if response.status == consumer.SUCCESS:
                print 'success'
                user = authenticate(openid_response=response)
                print 'user', user
                if user and user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/admin/')
            else:
                result = response.status
        return HttpResponse('error')

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
