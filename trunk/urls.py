from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^datos/(.*)$','django.views.static.serve',
{'document_root': 'datos/', 'show_indexes': True}),

)



