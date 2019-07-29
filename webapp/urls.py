from django.conf.urls import url
from . import views


app_name = 'webapp'

urlpatterns = [
    url('', views.base, name='base'),
    url(r'^base/', views.base, name='base'),
    url(r'^login/', views.login, name='login'),
    url(r'^signup/', views.signup, name='signup'),

    url(r'^delete/', views.delete, name='delete'),
    url(r'^blog_page/', views.blog_page, name='blog_page'),
    url(r'^post_page/', views.post_page, name='post_page'),

    url(r'^post_view/(?P<post_id>\d+)$', views.post_view, name='post_view'),
    #add
    url(r'^search/', views.search, name ='search'),
    url(r'^public_posts/', views.public_posts, name='public_posts'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^user_profile/(?P<user_id>\d+)$', views.user_profile, name='user_profile'),
    #url(r'^user_profile/', views.user_profile, name='user_profile'),
];

