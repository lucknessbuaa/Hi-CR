from django.core.urlresolvers import reverse  
from models import Jobs,Talk 
from base.models import City,Region,University
from tastypie import fields
from tastypie.constants import ALL,ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
import logging
import timestamp
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
        excludes = ['judge']
        filtering = {
            'id': ALL_WITH_RELATIONS,
            'name' : ALL_WITH_RELATIONS,
            'place' : ALL,
            'type' : ALL
        }
    def dehydrate(self,bundle):
        bundle.data['city_id'] = bundle.obj.place_id
        bundle.data['city_name'] = bundle.obj.place.name  
        return bundle

class InternResource(ModelResource):
    place = fields.ForeignKey(PlaceResource,'place')
    
    class Meta:
        queryset = Jobs.objects.filter(judge = 1)
        resource_name = 'intern' 
        allowed_methods = ['get']
        excludes = ['judge']
        filtering = { 
            'id': ALL_WITH_RELATIONS,
            'name' : ALL_WITH_RELATIONS,
            'place' : ALL,
            'type' : ALL 
        } 
    def dehydrate(self,bundle):
        bundle.data['city_id'] = bundle.obj.place_id  
        bundle.data['city_name'] = bundle.obj.place.name
        return bundle

class UniversityResource(ModelResource):
    city = fields.ForeignKey(PlaceResource,'city')
    class Meta:
        queryset = University.objects.all()
        resource_name = 'university'
        allowed_methods = ['get']

class TalkResource(ModelResource):
    class Meta:
        queryset = Talk.objects.all()
        resource_name = 'talk'
        allowed_methods = ['get']
        excludes = ['place','university','cover']
        filtering = { 
            'id':ALL,
            'date': ALL
        }
    def dehydrate(self,bundle):
        bundle.data['place_id'] = bundle.obj.university.city_id 
        bundle.data['place_name'] = bundle.obj.university.city
        bundle.data['university_id'] = bundle.obj.university.id
        bundle.data['university_name'] = bundle.obj.university
        bundle.data['date'] = timestamp(bundle.obj.date)
#        bundle.data['wtdate'] = bundle.obj.wtdate.strftime("%Y-%m-%d %H:%M:%S")
        bundle.data['wtdate'] = timestamp(bundle.obj.wtdate)
        bundle.data['location'] = bundle.obj.place
        bundle.data['url_picture'] ='hicr.limijiaoyin.com/media/'+ bundle.obj.cover
        return bundle
    def get_object_list(self,request):
        now = datetime.now()
        week = now + timedelta(days=7)
        mouth = now + timedelta(days=30)
        temp = super(TalkResource,self).get_object_list(request)
        if 'place' in request.GET:
            temp=temp.filter(university_id__city_id=request.GET['place']) 
        if 'order' in request.GET:
            temp=temp.order_by('date')
        if 'desc' in request.GET:
            temp=temp.order_by('-date')
        if 'week' in request.GET:
            temp=temp.filter(date__range=(now,week))
        else :
            if 'month' in request.GET:
                temp=temp.filter(date__range=(now,mouth))
            else :
                if 'finish' in request.GET:
                    temp=temp.filter(date__lte=now)
                else :
                    temp=temp.all()
        return temp
