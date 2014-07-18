from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from baidu import settings

import base.views

urlpatterns = patterns('',
    # Examples:
    url(r'^/?$', 'base.views.welcome'),
    url(r'^login$', 'base.views.login'),
    url(r'^login.json$','base.views.loginByJSON'),
    url(r'^logout$','base.views.logout'),
    url(r'^welcome$','base.views.welcome'),

    url(r'^ajax-upload/', include('ajax_upload.urls')),

    url(r'^backend/', include('backend.urls')),
    url(r'^api','backend.views.ajax_add')
    # url(r'^$', 'baidu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
