from django.conf.urls.defaults import patterns, url

from django_admin_sso.views import StartOpenIDView, FinishOpenIDView

urlpatterns = patterns('',

    url(r'^start/$', StartOpenIDView.as_view(), name='django_admin_sso.root'),
    url(r'^end/$', FinishOpenIDView.as_view(), name='django_admin_sso.return'),
)
