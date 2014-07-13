from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AdminSSOConfig(AppConfig):
    name = 'admin_sso'
    verbose_name = _("Admin Single Sign-On")
