from django.conf.urls import patterns, url
from blog import views

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^$', views.index, name='index')
)
