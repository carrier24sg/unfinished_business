from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, DetailView

from main.models import Project
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url('^$', TemplateView.as_view(template_name = "index.html")),
    url('^$', 'main.views.homepage'),
    # user logins
    url('^facebook/', include('django_facebook.urls')),
    url('^accounts/', include('django_facebook.auth_urls')),

    url('^me$', 'main.views.user_panel'),

    url('^project/(?P<pk>\d+)/$', DetailView.as_view(model = Project, context_object_name = "project", template_name='project/project_detail.html')),
    url('^project/create', 'main.views.create_new_project'),
    url('^project/(?P<pk>\d+)/apply/$', 'main.views.apply_project'),

    # url(r'^$', 'unfinished.views.home', name='home'),
    # url(r'^unfinished/', include('unfinished.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
