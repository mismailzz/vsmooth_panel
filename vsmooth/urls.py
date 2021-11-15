from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from patching import views

urlpatterns = [
    url(r'^$', views.index, name='index'), #function mapping to our application
    url(r'^vsmooth/$', views.index, name='index'),
    path('admin/', admin.site.urls),
    url(r'^vsmooth/', include('patching.urls')), #connect to urls of myfirstapp ~ ANOTHER WAY FOR IT
]
