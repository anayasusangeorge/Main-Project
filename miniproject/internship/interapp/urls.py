# from django.conf import settings
from django.urls import path

from interapp import views
# from django.conf.urls.static import static
#
# urlpatterns += static(settings.MEDIA_URL,
#                       document_root=settings.MEDIA_ROOT)

urlpatterns = [

    path('',views.index,name='index'),

    # path('LOGIN',views.LOGIN,name='LOGIN'),
    # path('REG',views.REG,name='REG'),
    path('login/',views.login,name='login'),
    path('register', views.register, name='register'),
    path('company', views.company, name='company'),
    path('students', views.students, name='students'),
    path('student_details/<int:id>/', views.student_details, name='student_details'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('courses/',views.courses,name='courses'),
    path('course-details/<slug:course_slug>/',views.course_details,name='course_details'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('pricing/',views.pricing,name='pricing'),
    path('trainers/',views.trainer,name='trainer'),
    path('logout/',views.logout,name='logout'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('enroll_course/',views.enroll_course,name='enroll_course'),
    path('endroll/<slug:course_slug>/',views.Course_endroll,name='endroll'),
    path('profile/',views.profile,name='profile'),
    path('searchbar/',views.searchbar,name='searchbar'),
    path('profile/update',views.profile_update,name='profile_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('paymentapproved/<str:leave_id>',views.paymentapproved,name='paymentapproved'),
    path('paymentdisapprove/<str:leave_id>', views.paymentdisapprove,name="paymentdisapprove"),
    path('orders/', views.courses, name='orders'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('subjects/', views.subjects, name='subjects'),
    path('add_subjects/', views.add_subjects, name='add_subjects'),
    path('subject_details/<int:id>/', views.subject_details, name='subject_details'),
    path('feedback/', views.feedback, name='feedback'),
    path('student_feedback_save', views.student_feedback_save, name="student_feedback_save"),

]