from django.shortcuts import render_to_response
from django.template import RequestContext
from sif.apps.inventario.forms import *
from sif.apps.reportes.forms import *
from sif.apps.inventario.models import *
from sif.apps.home.models import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from datetime import date
from reportlab.pdfgen import canvas
from django.http import HttpResponse

#lista reportes
def reportes_view(request):
	return render_to_response('reportes/lista_reportes.html', context_instance = RequestContext(request))

#reporte entrada
def reporte_view_entrada(request): 
	fecha = date.today()
	formulario = busqueda_form()
	bandera = "entrada"
	sedes = Sede.objects.all()
	if request.method == 'POST':
		formulario = busqueda_form(request.POST)
		sede = request.POST['sede']
		if formulario.is_valid():
			fecha_inicio = formulario.cleaned_data['fecha_inicio']
			fecha_fin = formulario.cleaned_data['fecha_fin']
			if str(fecha_inicio) > str(fecha):
				men = "La fecha de inicio no puede ser mayor a la fecha actual"
				print men
				ctx = {'sedes':sedes,'form': formulario, 'men': men}
				return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))
			if str(fecha_fin) < str(fecha_inicio): 
				men = "La fecha final no puede ser menor a la fecha inicial"
				ctx = {'sedes':sedes,'form': formulario, 'men': men}
				return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))
			lista_reporte = Entrada.objects.filter(fecha_ingreso__range=(str(fecha_inicio), str(fecha_fin)), sede__nombre_sede = sede)
			sede_id = Sede.objects.get(nombre_sede = sede).id
			men = ""			
			ctx = {'sede_id':sede_id,'sedes':sedes,'repor': lista_reporte,'form': formulario, 'ban': bandera, 'men':men, 'fecha_inicio':fecha_inicio,'fecha_fin':fecha_fin}
			return render_to_response('reportes/reporte.html',ctx, context_instance = RequestContext(request))
	ctx = {'form': formulario,'sedes':sedes}
	return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))


#reporte salida
def reporte_view_salida(request): 
	fecha = date.today()
	formulario = busqueda_form()
	bandera = "salida"
	sedes = Sede.objects.all()
	if request.method == 'POST':
		formulario = busqueda_form(request.POST)
		sede = request.POST['sede']
		if formulario.is_valid():
			fecha_inicio = formulario.cleaned_data['fecha_inicio']
			fecha_fin = formulario.cleaned_data['fecha_fin']
			if str(fecha) < str(fecha_inicio):
				men = "La fecha de inicio no puede ser mayor a la fecha actual"
				ctx = {'sedes':sedes,'form': formulario, 'men': men}
				return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))
			if str(fecha_fin) < str(fecha_inicio) : 
				men = "La fecha final no puede ser menor a la fecha inicial"
				ctx = {'sedes':sedes,'form': formulario, 'men': men}
				return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))
			lista_reporte = Salida.objects.filter(fecha_salida__range=(fecha_inicio, fecha_fin), sede__nombre_sede = sede)	
			men = ""
			sede_id = Sede.objects.get(nombre_sede = sede).id
			ctx = {'sede_id':sede_id,'sedes':sedes,'repor': lista_reporte,'form': formulario ,'ban': bandera,'men':men,'fecha_inicio':fecha_inicio,'fecha_fin':fecha_fin}
			return render_to_response('reportes/reporte.html',ctx, context_instance = RequestContext(request))
	ctx = {'form': formulario,'ban':bandera, 'sedes':sedes}
	return render_to_response('reportes/reporte.html',ctx , context_instance=RequestContext(request))


#Genera el pdf del reporte
def generar_pdf_view(request, fecha_inicio, fecha_fin, tipo, sede):
	if request.user.is_authenticated() and request.user.is_superuser == True:
		fecha = date.today()
		if tipo == "salida":
			lista_reporte = Salida.objects.filter(fecha_salida__range=(fecha_inicio, fecha_fin), sede__id = sede)	
		else:
			lista_reporte = Entrada.objects.filter(fecha_ingreso__range=(str(fecha_inicio), str(fecha_fin)), sede__id = sede)

		response = HttpResponse(mimetype='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=reporte.pdf'
		
		c = canvas.Canvas(response)
		y_1 = 700
		y_2 = 670
		y_3 = 680
		bandera = 1
		for p in lista_reporte:
			c.drawString(55,y_3,str(p.id))
			c.drawString(157,y_3,p.producto.nombre)
			c.drawString(295,y_3,str(p.cantidad))
			if tipo == "salida":
				c.drawString(360,y_3,p.tipo_salida)
				c.drawString(465,y_3,str(p.fecha_salida))
			else:
				c.drawString(360,y_3,p.referencia.razon_social.ciudad)
				c.drawString(465,y_3,str(p.fecha_ingreso))
			c.line(50,y_1,50,y_2)
			c.line(153,y_1,153,y_2)
			c.line(253,y_1,253,y_2)
			c.line(353,y_1,353,y_2)
			c.line(453,y_1,453,y_2)
			c.line(550,y_1,550,y_2)
			y_1 = y_1 - 30
			y_3 = y_3 - 30
			c.line(50,y_2,550,y_2)
			y_2 = y_2 - 30
			if y_2 < 100:
				y_1 = 700
				y_2 = 670
				y_3 = 680		
				ban = 1	
				c.showPage()
			if bandera == 1:
				c.drawString(250,800, "Funerales La Ermita")
				
				if tipo =="salida":
					c.drawString(55,710,"No. Salida")
					c.drawString(370,710,"Tipo Salida")
					c.drawString(465,710,"Fecha Salida")
					c.drawString(200,770, "REPORTE DE SALIDA DE COFRES")
				else:
					c.drawString(55,710,"No. Entrada")
					c.drawString(370,710,"Referencia")
					c.drawString(465,710,"Fecha Entrada")
					c.drawString(200,770, "REPORTE DE ENTRADA DE COFRES")
				c.drawString(175,710,"Producto")
				c.drawString(275,710,"Cantidad")

				c.line(50,730,550,730)
				c.line(50,700,550,700)
				c.line(50,730,50,700)
				c.line(153,730,153,700)
				c.line(253,730,253,700)
				c.line(353,730,353,700)
				c.line(453,730,453,700)
				c.line(550,730,550,700)

				c.drawString(50,70,"Fecha de generacion "+ str(fecha))
				c.drawString(50,50,"Reporte realizado entre "+ str(fecha_inicio) + "/" + str(fecha_fin))
				c.drawString(50,30,"Sede " + Sede.objects.get(id = sede).nombre_sede)
				bandera = 2
		c.showPage()
		c.save()
		return response
	else:
		return render_to_response('reportes/reporte.html', context_instance=RequestContext(request))

