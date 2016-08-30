from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^addfriend/(?P<id>\d+)$', views.addfriend),
    url(r'^friends$', views.friends),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^user/(?P<id>\d+)$', views.user),


]
