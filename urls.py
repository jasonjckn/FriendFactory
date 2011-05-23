from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^friendfactory/', include('friendfactory.foo.urls')),
    (r'^auth', 'main.views.auth'),

    (r'^landing$', 'main.views.landing'),
    (r'^landing_live/', 'main.views.landing_live'),
    (r'^ajax/set_compatibility', 'main.views.set_compatibility'),

    (r'^matches', 'main.views.matches'),
    (r'^ajax/matches', 'main.views.ajax_matches'),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':  settings.STATIC_DOC_ROOT}),


    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
