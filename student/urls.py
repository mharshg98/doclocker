from django.contrib import admin
from django.urls import path
from student import views

urlpatterns = [
    path('',views.login,name='login'),
    path('redirect',views.redirect,name='redirect'),
]

