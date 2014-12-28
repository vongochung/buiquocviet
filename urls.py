# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
import dbindexer
from django.conf.urls import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from home.models import POST,Category
from django.views.generic.simple import direct_to_template

info_dict = {
    'queryset': POST.objects.all().order_by('-date'),
    'date_field': 'date'
}
category_dict = {
    'queryset': Category.objects.all(),
}
sitemaps = {
    'post': GenericSitemap(info_dict, priority=0.6),
    'category': GenericSitemap(category_dict, priority=0.6)
}
handler500 = 'djangotoolbox.errorviews.server_error'
# django admin
admin.autodiscover()
# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
	('^admin-ngudan/vui-len-di-nao/', include(admin.site.urls)),
	(r'^robots\.txt$', direct_to_template,{'template': 'robots.txt', 'mimetype': 'text/plain'}),
	(r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^mce_filebrowser/', include('mce_filebrowser.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^sitemap\.xml/$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'', include('home.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {"template_name":"home/login.html"}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {"next_page" : "/"}),

)
