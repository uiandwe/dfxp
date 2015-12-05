from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
                       url(r'^$', views.Index, name='index'),
                       url(r'^upload/', views.upload, name='upload'),
                       url(r'^error/', views.error, name='error')

)
