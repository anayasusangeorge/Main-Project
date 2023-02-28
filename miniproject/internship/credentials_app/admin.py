from django.contrib import admin
from credentials_app.models import  user_reg,courses,user_logins

# Register your models here.
admin.site.register(user_reg)
admin.site.register(courses)
admin.site.register(user_logins)