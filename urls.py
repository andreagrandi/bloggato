from django.conf.urls import patterns, url, include

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^blog/', include('blog.urls')),
    ('^login/$', 'django.contrib.auth.views.login'),
    ('^logout/$', 'django.contrib.auth.views.logout'),
)
