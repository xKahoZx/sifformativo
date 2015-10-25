from django.shortcuts import render_to_response
from django.template import RequestContext
from sif.apps.inventario.forms import *
from sif.apps.reportes.forms import *
from sif.apps.inventario.models import *
from django.http import HttpResponseRedirect
from datetime import date

#lista reportes
def reportes_view(request):
	return render_to_response('reportes/lista_reportes.html', context_instance = RequestContext(request))

#reporte entrada
def reporte_view_entrada(request): 
	fecha = date.today()
	formulario = busqueda_form()
	bandera = "entrada"
	if request.method == 'POST':
		formulario = busqueda_form(request.POST)
		if formulario.is_valid():
			fecha_inicio = formulario.cleaned_data['fecha_inicio']
			fecha_fin = formulario.cleaned_data['fecha_fin']
			if str(fecha_inicio) > str(fecha):
				men = "La fecha de inicio no puede ser mayor a la fecha actual"
				print men
				ctx = {'form': formulario, 'men': men}
				return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))
			if str(fecha_fin) < str(fecha_inicio) : 
				men = "La fecha final no puede ser menor a la fecha inicial"
				ctx = {'form': formulario, 'men': men}
				return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))
			lista_reporte = Entrada.objects.filter(fecha_ingreso__range=(str(fecha_inicio), str(fecha_fin)))		
			ctx = {'repor': lista_reporte,'form': formulario, 'ban': bandera}
			return render_to_response('reportes/reporte.html',ctx, context_instance = RequestContext(request))
	ctx = {'form': formulario}
	return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))


#reporte salida
def reporte_view_salida(request): 
	fecha = date.today()
	formulario = busqueda_form()
	bandera = "salida"
	if request.method == 'POST':
		formulario = busqueda_form(request.POST)
		if formulario.is_valid():
			fecha_inicio = formulario.cleaned_data['fecha_inicio']
			fecha_fin = formulario.cleaned_data['fecha_fin']
			if str(fecha) < str(fecha_inicio):
				men = "La fecha de inicio no puede ser mayor a la fecha actual"
				ctx = {'form': formulario, 'men': men}
				return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))
			if str(fecha_fin) < str(fecha_inicio) : 
				men = "La fecha final no puede ser menor a la fecha inicial"
				ctx = {'form': formulario, 'men': men}
				return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))
			lista_reporte = Salida.objects.filter(fecha_salida__range=(fecha_inicio, fecha_fin))		
			ctx = {'repor': lista_reporte,'form': formulario ,'ban': bandera}
			return render_to_response('reportes/reporte.html',ctx, context_instance = RequestContext(request))
	ctx = {'form': formulario}
	return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))
