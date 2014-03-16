from django.conf.urls import patterns, include, url
from antibiobank import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'antibiobank.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name="home"),
    url(r'^ajax_bacteries.json$', views.ajax_bacteries, name="ajax_bacteries"),
    url(r'^ajax_specimens.json$', views.ajax_specimens, name="ajax_specimens"),
    url(r'^ajax_services.json$', views.ajax_services, name="ajax_services"),
    url(r'^ajax_stats.json$', views.ajax_stats, name="ajax_stats"),




    )
