from django.urls import path
from credentials_app import views

urlpatterns = [

    path('LOGIN',views.LOGIN,name='LOGIN'),
    path('REG',views.REG,name='REG'),
    path('login/',views.login,name='login'),
    path('register', views.register, name='register'),
    path('Home',views.Home,name='Home'),
    path('home/',views.home,name='home'),
]
