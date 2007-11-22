from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^admin/', include('django.contrib.admin.urls')),
	#(r'^wiki/', include('abuelas.wiki.urls')),
	(r'^datos/(.*)$','django.views.static.serve',{'document_root': 'datos/', 'show_indexes': True}),
	(r'^juzgados/$', 'abuelas.seguimiento.views.juzgados'),
	(r'^juzgados/(?P<juzgado_id>\d+)/$', 'abuelas.seguimiento.views.juzgados_detalle'),
	(r'^causas/$', 'abuelas.seguimiento.views.causas'),
	(r'^causas/(?P<causa_id>\d+)/$', 'abuelas.seguimiento.views.causa_detalle'),
	

)



