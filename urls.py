from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from blog import views

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    #url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^$', views.index, name='index')
)
