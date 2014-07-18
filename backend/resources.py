from django.core.urlresolvers import reverse  
from models import Jobs 
from base.models import City,Region
from tastypie import fields
from tastypie.constants import ALL,ALL_WITH_RELATIONS
from tastypie.resources import ModelResource


class RegionResource(ModelResource):
    
    class Meta:
        queryset = Region.objects.all()
        resource_name = 'region'

class PlaceResource(ModelResource):

    region = fields.ForeignKey(RegionResource,'region')
    class Meta:
        queryset = City.objects.all()
        resource_name = 'place'



class JobsResource(ModelResource):
    place = fields.ForeignKey(PlaceResource,'place')
    
    class Meta:
        queryset = Jobs.objects.filter(judge = 0)
        resource_name = 'jobs'
        allowed_methods = ['get']
        filtering = {
            'id': ALL_WITH_RELATIONS,
            'name' : ALL_WITH_RELATIONS,
            'place' : ALL,
            'type' : ALL
        }

class InternResource(ModelResource):
    place = fields.ForeignKey(PlaceResource,'place')
    
    class Meta:
        queryset = Jobs.objects.filter(judge = 1)
        resource_name = 'intern' 
        allowed_methods = ['get']
        filtering = { 
            'id': ALL_WITH_RELATIONS,
            'name' : ALL_WITH_RELATIONS,
            'place' : ALL,
            'type' : ALL 
        }   
#class TalkResource(ModelResource):
    
