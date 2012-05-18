from django.contrib import admin

from django_sso.models import Assignment


class AssignmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Assignment, AssignmentAdmin)
print admin.site.login_template
admin.site.login_template = 'django_sso/login.html'
