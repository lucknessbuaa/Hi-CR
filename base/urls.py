from django.conf.urls import patterns, include, url

import base.views

urlpatterns = patterns('',
    # Examples:
    url(r'^/?$', 'base.views.welcome'),
    url(r'^login$', 'base.views.login'),
    url(r'^login.json$','base.views.loginByJSON'),
    url(r'^logout$','base.views.logout'),
    url(r'^welcome$','base.views.welcome'),

    url(r'^backend/', include('backend.urls')),
    # url(r'^$', 'baidu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
)
