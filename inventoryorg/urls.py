from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [

    path('', views.loginuser, name="login"),
    path('/', views.loginuser, name="login"),
    path('login', views.loginuser, name="login"),
    path('load_serial/', views.load_serial, name="load_serial"),

    path('adminac/<int:value>/', views.adminac, name="adminac"),
    path('adminac/<int:value>/<str:pk>/', views.adminac, name="adminac"),

    path('managerac/<int:value>/', views.managerac, name="managerac"),
    path('managerac/<int:value>/<str:pk>/', views.managerac, name="managerac"),

    path('staffac/<int:value>/', views.staffac, name="staffac"),
    path('staffac/<int:value>/<str:pk>/', views.staffac, name="staffac"),

    path('logoutuser', views.logoutuser, name="logoutuser"),
    re_path(r'./logoutuser$', views.logoutuser, name="logoutuser"),
]
