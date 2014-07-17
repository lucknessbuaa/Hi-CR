from django.conf.urls import patterns, include, url
from resources import *
import views
from tastypie.api import Api


v1_api = Api(api_name = 'v1')
v1_api.register(RegionResource())
v1_api.register(PlaceResource())
v1_api.register(JobsResource())
v1_api.register(InternResource())
v1_api.register(TalkResource())
v1_api.register(UniversityResource())

urlpatterns = patterns('backend.talk_views', 
    url(r'^talk$', 'talk'),
    url(r'^talk/add$', 'add_talk'),
    url(r'^talk/delete$', 'delete_talk'),
    url(r'^talk/requireUni$', 'requireUni'),
    url(r'^talk/requireCity$', 'requireCity'),
    url(r'^talk/(?P<id>\d+)$', 'edit_talk'),
)

urlpatterns = urlpatterns + patterns('backend.jobs_views',
    url(r'^jobs$','jobs'),
    url(r'^jobs/add$','add_jobs'),
    url(r'^jobs/delete$','delete_jobs'),
    url(r'^jobs/(?P<id>\d+)$','edit_jobs'),
    url(r'^api/',include(v1_api.urls)),
)

