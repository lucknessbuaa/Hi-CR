from django.conf.urls import patterns, include, url

urlpatterns = patterns('backend.talk_views', 
    url(r'^talk$', 'talk'),
)

urlpatterns = urlpatterns + patterns('backend.jobs_views',
    url(r'^jobs$','jobs'),
    url(r'^jobs/add$','add_jobs'),
    url(r'^jobs/delete$','delete_jobs'),
    url(r'^jobs/(?P<id>\d+)$', 'edit_jobs'),
)
