# encoding: utf-8
from django.core.management.base import BaseCommand, CommandError
from base.models import University, City, Region

data = [{
    'name': u'华北',
    'cities': [{
        'name': u'北京',
        'universities': [
            u'北京大学', 
            u'清华大学', 
            u'中国科学院大学', 
            u'北京航空航天大学', 
            u'北京理工大学', 
            u'北京邮电大学', 
            u'北京外国语大学', 
            u'对外经济贸易大学'
        ]
    }, {
        'name': u'天津',
        'universities': [
            '天津大学',
            '南开大学',
            '天津外国语大学'
        ]
    }]
},{
    'name': u'华东',
    'cities': [{
        'name': u'上海',
        'universities': [
            u'复旦大学',
            u'上海交通大学',
            u'上海外国语大学'
        ]
    },{
        'name': u'南京',
        'universities': [
            u'南京大学',
            u'东南大学'
        ]
    }, {
        'name': u'合肥',
        'universities': [
            u'中国科学技术大学'
        ]
    }, {
        'name': u'杭州',
        'universities': [
            u'浙江大学'
        ]
    }, {
        'name': u'济南',
        'universities': [
            u'山东大学'
        ]
    }]
}, {
    'name': u'华中',
    'cities': [{
        'name': u'武汉',
        'universities': [
            u'武汉大学',
            u'华中科技大学'
        ]
    },{
        'name': u'长沙',
        'universities': [
            u'中南大学'
        ]
    }]
}, {
    'name': u'华南',
    'cities': [{
        'name': u'广州',
        'universities': [
            u'中山大学',
            u'华南理工大学',
            u'广东外语外贸大学'
        ]
    },{
        'name': u'厦门',
        'universities': [
            u'厦门大学'
        ]
    }, {
        'name': u'深圳',
        'universities': [
            u'哈工大深圳研究生院'
        ]
    }]
}, {
    'name': u'东北',
    'cities': [{
        'name': u'哈尔滨',
        'universities': [
            u'哈尔滨工业大学',
            u'哈尔滨工程大学'
        ]
    },{
        'name': u'长春',
        'universities': [
            u'吉林大学'
        ]
    }, {
        'name': u'沈阳',
        'universities': [
            u'东北大学'
        ]
    }, {
        'name': u'大连',
        'universities': [
            u'大连理工大学'
        ]
    }]
}, {
    'name': u'西北',
    'cities': [{
        'name': u'西安',
        'universities': [
            u'西安交通大学',
            u'西安电子科技大学',
            u'西安外国语大学'
        ]
    }]
}, {
    'name': u'西南',
    'cities': [{
        'name': u'成都',
        'universities': [
            u'四川大学'
        ]
    }]
}]

class Command(BaseCommand):

    def handle(self, *args, **options):
        Region.objects.all().delete()

        for _region in data:
            region = Region(name=_region['name'])
            region.save()

            for _city in _region['cities']:
                city = City(region=region, name=_city['name'])
                city.save()

                for _university in _city['universities']:
                    University(city=city, name=_university).save()
