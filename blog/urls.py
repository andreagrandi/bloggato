from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new_post, name='post-new'),
    url(r'^(?P<id>\d+)/$', views.view_post, name='post-detail'),
    url(r'^(?P<id>\d+)/edit/$', views.modify_post, name='post-modify'),
    url(r'^(?P<id>\d+)/delete/$', views.delete_post, name='post-delete'),
)
