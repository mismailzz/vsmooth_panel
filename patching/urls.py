from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from patching import views

urlpatterns = [
    #url(r'^patch/$', views.vm_patch, name='vm_patch'), #function mapping to our application
    url(r'^patch/$', views.connect_select_patch, name="connect_select_patch"),
]
