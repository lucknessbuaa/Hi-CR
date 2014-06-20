from django.conf.urls import patterns, include, url

urlpatterns = patterns('backend.xuanjiang_views', 
    url(r'^xuanjiang$', 'xuanjiang'),
)
