from django.conf.urls import patterns, url

from django_sso.views import StartOpenIDView, FinishOpenIDView

urlpatterns = patterns('',

    url(r'^start/$', StartOpenIDView.as_view(), name='django_sso.root'),
    url(r'^end/$', FinishOpenIDView.as_view(), name='django_sso.return'),
)
