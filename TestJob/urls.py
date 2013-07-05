from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('main.views',
    (r'^$', 'main'),
    (r'^xhr_getUsers/$','xhr_getUsers'),
    (r'^xhr_getRooms/$','xhr_getRooms'),
    (r'^xhr_postUsers/$','xhr_postUsers'),
    (r'^xhr_editUsers/$','xhr_editUsers'),
    (r'^xhr_editRooms/$','xhr_editRooms'),
    (r'^xhr_postRooms/$','xhr_postRooms'),

)
