from django.utils.module_loading import import_module
from django.contrib.admin.apps import AdminConfig as DjangoAdminConfig


class AdminConfig(DjangoAdminConfig):
    default_site = "{{ cookiecutter.project_name }}.admin.sites.AdminSite"

    def ready(self):
        super().ready()
        import_module("{{ cookiecutter.project_name }}.admin.views")
