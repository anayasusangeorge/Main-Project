import csv
from django.contrib import admin
from django.http import HttpResponse
from interapp.models import User, user_course,duration,trainers,video,requirement,Payment,OrderPlaced,add_subject,FeedBackStudent




def export_details(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="User.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email','First Name','Last Name','Phonenumber'])
    courses = queryset.values_list('email','first_name','last_name','phonenumber')
    for i in courses:
        writer.writerow(i)
    return response
export_details.short_description = 'Export to csv'




class UserAdmin(admin.ModelAdmin):
    list_display=['email','first_name','last_name','phonenumber']
    actions = [export_details]
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def render_change_form(self, request, context, add=False, change=False,form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
admin.site.register(User,UserAdmin)

#

# Register your models here.
def export_details(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_course.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Course WEEK', 'Description'])
    courses = queryset.values_list('course_name', 'course_week', 'desc')
    for i in courses:
        writer.writerow(i)
    return response


export_details.short_description = 'Export to csv'

admin.site.register(duration)



class requirement_TabularInline(admin.TabularInline):
    model = requirement



class video_TabularInline(admin.TabularInline):
    model = video
class usercourseAdmin(admin.ModelAdmin):
    inlines = (video_TabularInline, requirement_TabularInline)
    list_display = ['course_name', 'image','course_week','price']
    actions = [export_details]

admin.site.register(user_course, usercourseAdmin)

admin.site.register(add_subject)

admin.site.register(Payment)

admin.site.register(OrderPlaced)
admin.site.register(FeedBackStudent)

