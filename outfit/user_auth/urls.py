from django.conf.urls import patterns, include, url
from user_auth import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'outfit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^closet_upload/', views.closet_upload, name='closet_upload'),
    url(r'^try/', views.trya, name='trya'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^userdetails/$', views.completeuserdetails, name='userdetails'),

)

