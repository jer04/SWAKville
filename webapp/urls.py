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

    url(r'^postview/(?P<post_id>\d+)$', views.post_view, name='postview'),
];

