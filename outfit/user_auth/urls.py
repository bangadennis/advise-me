from django.conf.urls import patterns, include, url
from user_auth import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'outfit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^register/$', views.register, name='register'),
    url(r'^try/', views.trya, name='trya'),
    
)

