from django.conf.urls import patterns, include, url

urlpatterns = patterns('backend.talk_views', 
    url(r'^talk$', 'talk'),
)

urlpatterns = urlpatterns + patterns('backend.zhaopin_views',
    url(r'^zhaopin$','pages'),
    url(r'^zhaopin/add$','add_page'),
    url(r'^zhaopin/delete$','delete_page'),
    url(r'^zhaopin/(?P<id>\d+)$', 'edit_page'),
)
