from django.conf.urls import patterns, url, include
from blog import views as blog_views

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^blog/', include('blog.urls')),
    ('^login/$', 'django.contrib.auth.views.login'),
    ('^logout/$', 'django.contrib.auth.views.logout'),
    url('^about/$', blog_views.about),
)
