from django.conf.urls import patterns, include, url

urlpatterns = patterns('backend.talk_views', 
    url(r'^talk$', 'talk'),
)

urlpatterns = urlpatterns + patterns('backend.zhaopin_views',
    url(r'^zhaopin$','pages')
)
