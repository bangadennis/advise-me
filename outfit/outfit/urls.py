from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'outfit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
     url(r'^$', 'user_auth.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('user_auth.urls')),
    url(r'^password/', include('password_reset.urls')),
    url(r'^ajaximage/', include('ajaximage.urls')),
    
)

#Media files

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )