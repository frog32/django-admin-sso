from django.conf.urls import patterns, url
from django.contrib import admin

from admin_sso import settings
from admin_sso.models import Assignment


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'username', 'username_mode', 'domain',
                    'user', 'weight')
    list_editable = ('username', 'username_mode', 'domain', 'user', 'weight')

    def get_urls(self):
        urls = super(AssignmentAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.module_name
        if settings.DJANGO_ADMIN_SSO_USE_OAUTH:
            my_urls = patterns('admin_sso.views',
                url(r'^start/$', 'start',
                    name='%s_%s_start' % info),
                url(r'^end/$', 'end',
                    name='%s_%s_end' % info),
            )
        else:
            from admin_sso.openid.views import StartOpenIDView, FinishOpenIDView
            my_urls = patterns('',
                url(r'^start/$', StartOpenIDView.as_view(),
                    name='%s_%s_start' % info),
                url(r'^end/$', FinishOpenIDView.as_view(),
                    name='%s_%s_return' % info),
            )
        return my_urls + urls

admin.site.register(Assignment, AssignmentAdmin)


class OpenIDUserAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'email', 'user')

if not settings.DJANGO_ADMIN_SSO_USE_OAUTH:
    from .openid.models import OpenIDUser
    admin.site.register(OpenIDUser, OpenIDUserAdmin)

if settings.DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON:
    admin.site.login_template = 'admin_sso/login.html'
