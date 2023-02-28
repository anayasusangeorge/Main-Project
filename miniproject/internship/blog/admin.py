from django.contrib import admin
from . import models


# Register your models here.



class BlogAdminArea(admin.AdminSite):
    site_header = 'Blog Database'

class TestAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


blog_site = BlogAdminArea(name='BlogAdmin')
blog_site.register(models.post, TestAdminPermissions)
