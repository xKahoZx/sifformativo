from django.conf.urls.defaults import patterns, url

urlpatterns = patterns ('sif.apps.reportes.views',
	url(r'^reporte_entrada/$','reporte_view_entrada', name = 'vista_reporte_entrada'),
	url(r'^reporte_salida/$','reporte_view_salida', name = 'vista_reporte_salida'),
	url(r'^lista_reportes/$','reportes_view', name = 'vista_reportes'),
	url(r"^pdf/(?P<fecha_inicio>[^/]+)/(?P<fecha_fin>[^/]+)/(?P<tipo>[^/]+)/(?P<sede>[^/]+)$", 'generar_pdf_view' , name = 'generar_pdf'),

)