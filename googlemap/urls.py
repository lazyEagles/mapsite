from django.conf.urls.defaults import*
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('googlemap.views',
    url(r'^$', 'index', name='googlemap-index'),
    url(r'^query/$', 'query', name='googlemap-query'),
    url(r'^region/$', 'region', name='googlemap-region'),
    url(r'^distance/$', 'distance', name='googlemap-distance'),
    url(r'^country/$', 'country', name='googlemap-country'),
    url(r'^population/$', 'population', name='googlemap-population'),
    url(r'^neighbor/$', 'neighbor', name='googlemap-neighbor'),
    url(r'^readme/$', 'readme', name='googlemap-readme'),
)
