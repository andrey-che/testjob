from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('main.views',
    (r'^$', 'main'),
    (r'^xhr_postRow/$','xhr_postRow'),
    (r'^xhr_getModel/$','xhr_getModel'),
    (r'^xhr_editField/$','xhr_editField'),
    (r'^xhr_getLastRow/$','xhr_getLastRow'),
)

