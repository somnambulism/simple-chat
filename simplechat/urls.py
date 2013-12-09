from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',  login, {'template_name': 'enter.jade'}),
    url(r'^logout/$', logout),
    url(r'^chat/$', 'apps.chat.views.view_chat'),
    url(r'^send/$', 'apps.chat.views.write_message'),
    url(r'^get-messages/$', 'apps.chat.views.get_messages'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.static',
    (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
)
