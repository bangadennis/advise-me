from django.conf.urls import patterns, include, url
from user_auth import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'outfit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #trial
    url(r'^google/$', views.google, name='google'),
    #urls
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^closet_upload/', views.closet_upload, name='closet_upload'),
    url(r'^dash/', views.dash, name='trya'),
    url(r'^logout/$', views.user_logout, name='logout'),
    
    url(r'^userdetails/$', views.completeuserdetails, name='userdetails'),
    url(r'^edit_userdetails/(?P<pk>\d+)$', views.UserDetailsUpdate.as_view(), name='edit_userdetails'),
    url(r'^add_user_activity/$', views.add_user_activity, name='add_user_activity'),
    url(r'^delete_activity/(?P<activity_id>\d+)/delete/$', views.delete_activity, name='delete_activity'),
    url(r'^user_activities/$', views.user_activites, name='user_activities'),
    
    url(r'^get_facts/(?P<cloth_id>\d+)/view/$', views.add_cloth_facts, name='cloth_facts'),
    url(r'^delete_cloth/(?P<cloth_id>\d+)/delete/$', views.delete_cloth, name='delete_cloth'),
    
    url(r'^update_cloth_facts/(?P<cloth_id>\d+)/view/$', views.update_cloth_facts, name='update_cloth_facts'),
    
    
     

)

