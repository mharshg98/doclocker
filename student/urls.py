from django.contrib import admin
from django.urls import path
from student import views

urlpatterns = [
    path('',views.login,name='login'),
    path('redirect1',views.redirect1,name='redirect1'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('receipt',views.receipt,name='receipt'),
    path('pointer',views.pointer,name='pointer'),
    path('profile',views.profile,name='profile'),

]

