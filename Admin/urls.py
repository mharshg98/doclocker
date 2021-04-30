from django.contrib import admin
from django.urls import path
from Admin import views

urlpatterns = [
    path('',views.login,name='login'),
    #path('register', views.register,name='register'),
    #path('login', views.login,name='login'),
    path('logout', views.logout,name='logout'),
]

