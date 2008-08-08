from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^abues/', include('abues.foo.urls')),

    # Uncomment the next line to enable admin documentation:
    (r'^doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    (r'^(.*)', admin.site.root),
)
