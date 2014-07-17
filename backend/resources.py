from django.core.urlresolvers import reverse  
from models import Jobs,Talk 
from base.models import City,Region,University
from tastypie import fields
from tastypie.constants import ALL,ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
import logging
from datetime import datetime,date,timedelta

logger = logging.getLogger('django')

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
    def dehydrate(self,bundle):
        bundle.data['city_id'] = bundle.obj.place_id  
        return bundle

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
    def dehydrate(self,bundle):
        bundle.data['city_id'] = bundle.obj.place_id  
        return bundle

class UniversityResource(ModelResource):
    city = fields.ForeignKey(PlaceResource,'city')
    class Meta:
        queryset = University.objects.all()
        resource_name = 'university'
        allowed_methods = ['get']

class TalkResource(ModelResource):
    university = fields.ForeignKey(UniversityResource,'university')
    class Meta:
        queryset = Talk.objects.all()
        resource_name = 'talk'
        allowed_methods = ['get']
        filtering = { 
            'id':ALL,
            'date': ALL
        }
    def dehydrate(self,bundle):
        bundle.data['city_id'] = bundle.obj.university.city_id 
        bundle.data['university_id'] = bundle.obj.university.id
        return bundle
    def get_object_list(self,request):
        now = datetime.now()
        week = now - timedelta(days=7)
        mouth = now - timedelta(days=30)
        temp = super(TalkResource,self).get_object_list(request)
        logger.debug(temp)
        if 'city_id' in request.GET:
            return temp.filter(university_id__city_id=request.GET['city_id'])
        else :  
            if 'week' in request.GET:
                logger.debug(date)
                return temp.filter(date__range=(week,now))
            else :
                if 'mouth' in request.GET:
                    return temp.filter(date__range=(mouth,now))
                else :
                    if 'finish' in request.GET:
                        return temp.filter(date__lte=now)
                    else :
                        return temp.all()
