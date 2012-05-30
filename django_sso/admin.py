from django.contrib import admin

from django_sso import settings
from django_sso.models import Assignment


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'username', 'username_mode', 'domain',
                    'user', 'weight')
    list_editable = ('username', 'username_mode', 'domain', 'user', 'weight')

admin.site.register(Assignment, AssignmentAdmin)

if settings.DJANGO_SSO_ADD_LOGIN_BUTTON:
    admin.site.login_template = 'django_sso/login.html'
