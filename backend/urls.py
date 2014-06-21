from django.conf.urls import patterns, include, url

urlpatterns = patterns('backend.xuanjiang_views', 
    url(r'^xuanjiang$', 'xuanjiang'),
)

urlpatterns = urlpatterns + patterns('backend.zhaopin_views',
    url(r'^zhaopin$','pages')
)
