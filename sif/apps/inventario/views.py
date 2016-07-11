from django.shortcuts import render_to_response
from django.core.exceptions import ValidationError
from django.template import RequestContext
import time
import datetime
from datetime import date
from sif.apps.inventario.forms import *
from sif.apps.inventario.models import *
from django.http import HttpResponseRedirect
from barcode.writer import ImageWriter
import barcode

#Sedes
def add_sede_view(request):
	info = "iniciando"
	if request.method=="POST":
		formulario = add_sede_form(request.POST, request.FILES) 
		if formulario.is_valid():
			add = formulario.save(commit = False)
			add.save()
			crear_productos_nueva_sede(add)
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect ('/sedes')
	else:
		formulario = add_sede_form()
	ctx = {'form':formulario,'informacion': info}
	return render_to_response('inventario/add_sede.html',ctx, context_instance = RequestContext(request))

def crear_productos_nueva_sede(sede):
	productos = Producto.objects.all().order_by('codigobarras')
	if productos:
		codigo_inicial = CodigoBarras.objects.get(id = 1)
		codigo_final = codigo_inicial
		tamanio = len(productos)
		producto_aux = Producto.objects.get(id = 1)
		producto_aux.id = tamanio + 1
		producto_aux.sede = sede
		producto_aux.cantidad = 0
		producto_aux.save()
		tamanio = tamanio + 1
		for p in productos:	
			if codigo_inicial != codigo_final:
				producto_aux = p
				producto_aux.id = tamanio + 1
				producto_aux.sede = sede
				producto_aux.cantidad = 0
				producto_aux.save()
				tamanio = tamanio + 1
			codigo_inicial = codigo_final
			codigo_final = p.codigobarras


def edit_sede_view(request, id_sede):
	info = ""
	sede = Sede.objects.get(pk =id_sede)
	if request.method == "POST":
		formulario = add_sede_form(request.POST, request.FILES,  instance= sede)
		if formulario.is_valid():
			edit_sede = formulario.save(commit = False)
			edit_sede.save()
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect('/sedes')
	else: 
		formulario = add_sede_form(instance = sede)
	ctx = {'form':  formulario, 'informacion': info}
	return  render_to_response('inventario/edit_sede.html', ctx, context_instance = RequestContext(request))

#Referencias
def add_refe_view(request):
	info = "iniciando"
	if request.method=="POST":
		formulario = add_refe_form(request.POST, request.FILES) 
		if formulario.is_valid():
			add = formulario.save(commit = False)
			add.save()
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect ('/referencias')
	else:
		formulario = add_refe_form()
	ctx = {'form':formulario,'informacion': info}
	return render_to_response('inventario/add_refe.html',ctx, context_instance = RequestContext(request))


def edit_refe_view(request, id_refe):
	info = ""
	refe = Referencia.objects.get(pk =id_refe)
	if request.method == "POST":
		formulario = add_refe_form(request.POST, request.FILES,  instance= refe)
		if formulario.is_valid():
			edit_refe = formulario.save(commit = False)
			edit_refe.save()
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect('/referencias')
	else: 
		formulario = add_refe_form(instance = refe)
	ctx = {'form':  formulario, 'informacion': info}
	return  render_to_response('inventario/edit_refe.html', ctx, context_instance = RequestContext(request))


#Entradas
def add_entrada_view(request):
	fecha = date.today()
	if request.method == "POST":
		formulario = add_entrada_form(request.POST)
		if formulario.is_valid():
			codigo = formulario.cleaned_data['codigobarras'] 
			sede = formulario.cleaned_data['sede']
			prod = Producto.objects.get(codigobarras__codigo = codigo, sede = sede)
			cant = formulario.cleaned_data['cantidad']
			add = formulario.save(commit = False)
			if (cant > 0):
				prod.cantidad = prod.cantidad + cant
				prod.save()
				add.producto = prod
				add.fecha_ingreso = fecha
				add.save()
				return HttpResponseRedirect('/entrada/%s' %add.id)
			else:
				formulario = add_entrada_form(instance = add)
				mensaje = "Error la cantidad debe ser mayor que 0"
				ctx = {'men':mensaje, 'form': formulario}
				return render_to_response('inventario/add_entrada.html', ctx, context_instance = RequestContext(request))
	else:
		formulario = add_entrada_form()
	ctx = {'form': formulario}
	return render_to_response('inventario/add_entrada.html', ctx, context_instance = RequestContext(request))

def edit_entrada_view(request, id_entr):
	entrada = Entrada.objects.get(pk =id_entr)
	cant_ini = entrada.cantidad
	prod = entrada.producto
	producto = entrada.producto.nombre
	productos = Producto.objects.filter(sede = 1)
	if request.method == "POST":
		formulario = edit_entrada_form(request.POST, request.FILES,  instance= entrada)
		if formulario.is_valid():			
			cant_fin = formulario.cleaned_data['cantidad']
			sede = formulario.cleaned_data['sede']
			nombre_producto = request.POST['producto']
			edit_entrada = formulario.save(commit = False)
			if cant_fin > 0 :
				prod_aux = Producto.objects.get(nombre = nombre_producto, sede = sede)
				if prod.id == prod_aux.id:
					if cant_ini > cant_fin:
						cant_tol = cant_ini - cant_fin
						prod.cantidad = prod.cantidad - cant_tol
						prod.save()				
						edit_entrada.save()
						info = "Guardado satisfactoriamente"
						return HttpResponseRedirect('/entrada/%s'% edit_entrada.id)	
					else:
						cant_tol = cant_fin - cant_ini
						prod.cantidad = prod.cantidad + cant_tol
						prod.save()					
						edit_entrada.save()
						info = "Guardado satisfactoriamente"
						return HttpResponseRedirect('/entrada/%s'% edit_entrada.id)					
				else:
					prod.cantidad = prod.cantidad - cant_ini
					prod_aux.cantidad = prod_aux.cantidad + cant_fin
					prod.save()
					prod_aux.save()
					edit_entrada.producto = prod_aux
					edit_entrada.sede = sede
					edit_entrada.save()				
					return HttpResponseRedirect('/entrada/%s'% edit_entrada.id)
			else:
				formulario = edit_entrada_form(instance = entrada)
				mensaje = "Error, la cantidad debe ser mayor que o igual que 0"
				ctx = {'form':  formulario, 'productos':productos, 'produc_ini':producto,'men':mensaje}				
				return  render_to_response('inventario/edit_entrada.html', ctx, context_instance = RequestContext(request))
	else: 
		formulario = edit_entrada_form(instance = entrada)		
	ctx = {'form':  formulario, 'productos':productos, 'produc_ini':producto}
	return  render_to_response('inventario/edit_entrada.html', ctx, context_instance = RequestContext(request))


#Salida
def add_salida_view(request):
	fecha = date.today()		
	if request.method == 'POST':
			formulario = add_salida_form(request.POST)
			if formulario.is_valid():
				sede = formulario.cleaned_data['sede']
				codigo = formulario.cleaned_data['codigobarras']				
				prod = Producto.objects.get(codigobarras__codigo = codigo, sede = sede)
				cant = formulario.cleaned_data['cantidad']
				aux =  prod.cantidad - cant
				add = formulario.save(commit = False)
				if (aux >= 0 and cant > 0):
					prod.cantidad = aux
					prod.save()
					add.producto = prod
					add.fecha_salida = fecha
					add.save()
					return HttpResponseRedirect('/salida/%s' %add.id)
				else:
					if cant <= 0:
						mensaje = "La cantidad de salida debe ser mayor a 0"
					else:	
						mensaje = "No se puede agregar esta salida la cantidad no esta disponible"
					formulario = add_salida_form()
					ctx = {'men':mensaje, 'form': formulario}
					return render_to_response('inventario/add_salida.html', ctx, context_instance = RequestContext(request))
			else:
					
					ctx = {'form': formulario}
					return render_to_response('inventario/add_salida.html', ctx, context_instance = RequestContext(request))
	else:
		formulario = add_salida_form()
		ctx = {'form': formulario}
		return render_to_response('inventario/add_salida.html', ctx , context_instance = RequestContext(request))


def edit_salida_view(request, id_sal):
	sali = Salida.objects.get(id = id_sal)
	cant_ini = sali.cantidad
	prod = sali.producto
	producto = sali.producto.nombre
	productos = Producto.objects.filter(sede = 1)
	if request.method == 'POST':
		formulario = edit_salida_form(request.POST, request.FILES, instance = sali)
		if formulario.is_valid():
			cant_fin = formulario.cleaned_data['cantidad']			
			edit_sal = formulario.save(commit = False)
			if cant_fin > 0:				
				sede = formulario.cleaned_data['sede']
				nombre_producto = request.POST['producto']
				prod_aux = Producto.objects.get(nombre = nombre_producto, sede = sede)
				if prod.id == prod_aux.id:
					if cant_ini > cant_fin:
						cant_tol = cant_ini - cant_fin
						prod.cantidad = prod.cantidad + cant_tol
						prod.save()				
						edit_sal.save()
						info = "Guardado satisfactoriamente"
						return HttpResponseRedirect('/salida/%s'% edit_sal.id)	
					else:
						cant_tol = cant_fin - cant_ini
						prod.cantidad = prod.cantidad - cant_tol
						if prod.cantidad >= 0:
							prod.save()					
							edit_sal.save()
							info = "Guardado satisfactoriamente"
							return HttpResponseRedirect('/salida/%s'% edit_sal.id)
						else:
							formulario = edit_salida_form(instance = edit_sal)
							mensaje = "No se puede agregar esta salida la cantidad no esta disponible"
							ctx = {'men':mensaje, 'form': formulario}
							return render_to_response('inventario/add_salida.html', ctx, context_instance = RequestContext(request))
				else:
					prod.cantidad = prod.cantidad + cant_ini
					prod_aux.cantidad = prod_aux.cantidad - cant_fin
					if prod_aux.cantidad >= 0:
						prod.save()
						prod_aux.save()
						edit_sal.producto = prod
						edit_sal.sede = sede
						edit_sal.save()				
						return HttpResponseRedirect('/salida/%s'% edit_sal.id)
					else:
						formulario = edit_salida_form(instance = edit_sal)
						mensaje = "No se puede agregar esta salida la cantidad no esta disponible"
						ctx = {'form':  formulario, 'productos':productos, 'produc_ini':producto,'men':mensaje}
						return render_to_response('inventario/edit_salida.html', ctx, context_instance = RequestContext(request))	
			else:
				formulario = edit_salida_form(instance = sali)
				mensaje = "Error, la cantidad debe ser mayor que o igual que 0"
				ctx = {'form':  formulario, 'productos':productos, 'produc_ini':producto, 'men':mensaje}
				return  render_to_response('inventario/edit_salida.html', ctx, context_instance = RequestContext(request))
			
	else:
		formulario = edit_salida_form(instance = sali)
	ctx = {'form':  formulario, 'productos':productos, 'produc_ini':producto}
	return render_to_response('inventario/edit_salida.html', ctx , context_instance = RequestContext(request))

#Proveedor

def add_prove_view(request):
	info = "iniciando"
	if request.method=="POST":
		formulario = add_prove_form(request.POST, request.FILES) 
		if formulario.is_valid():
			add = formulario.save(commit = False)
			add.save()
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect ('/proveedores/')
	else:
		formulario = add_prove_form()
	ctx = {'form':formulario,'informacion': info}
	return render_to_response('inventario/add_proveedor.html',ctx, context_instance = RequestContext(request))


def edit_prove_view(request, id_prov):
	info = ""
	proveedor = Proveedor.objects.get(pk =id_prov)
	if request.method == "POST":
		formulario = add_prove_form(request.POST, request.FILES,  instance= proveedor)
		if formulario.is_valid():
			edit_prov = formulario.save(commit = False)
			edit_prov.save()
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect('/proveedores/')
	else: 
		formulario = add_prove_form(instance = proveedor)
	ctx = {'form':  formulario, 'informacion': info}
	return  render_to_response('inventario/edit_proveedor.html', ctx, context_instance = RequestContext(request))




#Producto

def add_product_view(request):
	info = "inicializando"
	if request.method == "POST":
		formulario = add_product_form(request.POST, request.FILES)
		if formulario.is_valid():
			add = formulario.save(commit = False)
			add.codigobarras = creaCodigoAux()
			add.sede = Sede.objects.get(id = 1)	
			add.save()
			id_prod = add.id - 1		
			crear_producto_sedes(add)
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/producto/%s' %id_prod)
	else:
		formulario = add_product_form()
	ctx = {'form':formulario,'informacion':info}
	return render_to_response('inventario/add_product.html', ctx,context_instance = RequestContext(request))

def crear_producto_sedes(add):
	sedes = Sede.objects.all()	
	for p in sedes:
		add.sede = p
		add.save()		
		add.id = add.id + 1  
	
def edit_product_view(request, id_prod):
	info = ""
	prod = Producto.objects.get(pk = id_prod)
	if request.method == "POST":
		formulario = add_product_form(request.POST, request.FILES, instance= prod)
		if  formulario.is_valid():
			edit_prod = formulario.save(commit = False)
			formulario.save_m2m()
			edit_prod.save()
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/producto/%s'% edit_prod.id)
	else:
		formulario = add_product_form(instance = prod)
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response ('inventario/edit_product.html', ctx,context_instance = RequestContext(request))

def del_product_view(request, id_prod):
	
	info = "inicializando"
	try:
		prod = Producto.objects.get(pk = id_prod)
		prod.delete()
		info = "Producto Eliminado Correctamente"
		return HttpResponseRedirect('/producto/')
	except:
		info = "Producto no se puede eliminar"	
		return HttpResponseRedirect('/producto/')


#Codigo barras

'''
 La vista creaCodigo: Crea un codigo sin necesidad de formulario, solo le hace falta 
 hacer un request post y automaticamente genera un codigo con ID unico y redirige a otro template
 donde se ve el codigo y la imagen del codigo generado 
'''
def creaCodigo(request):
	
	informacion = "Inicia"
	if request.method == "POST":
		formulario = FormuCrea(request.POST)
		if formulario.is_valid():
			informacion = "pasa post"
			EAN = barcode.get_barcode_class('ean13')
			
			codigo = formulario.cleaned_data['codigo'] 
			ean = barcode.get_barcode('ean', codigo, writer=ImageWriter())
			aux = int(codigo) / 10
			ean.save("sif/media/codes/" + str(aux))
			crea = CodigoBarras(codigo = aux)			
			crea.save()		
			
			informacion = "Terminado"
        
			return HttpResponseRedirect('/codigoBarras/%s' %crea.id)
	else:
		formulario = FormuCrea()
		
	ctx = {'form': formulario,'info':informacion}
	return render_to_response('inventario/agregaCB.html',ctx,context_instance = RequestContext(request))


def creaCodigoAux():
	
	stamp = str(int(time.time() * 1000))[:12]
	ean = barcode.get_barcode('ean', stamp, writer=ImageWriter())
	ean.save("sif/media/codes/" + stamp)
	crea = CodigoBarras(codigo=stamp)
	crea.save()
	cofre = CodigoBarras.objects.get(id=crea.id)
	return cofre
	
'''
  La vista ver_unico: Muestra un codigo de barras y su imagen en base a su id 
'''
def ver_unico(request,id_cofre):
	cofre = CodigoBarras.objects.get(id=id_cofre)
	ctx = {'cofre':cofre}
	return render_to_response('inventario/muestraProducto.html',ctx,context_instance = RequestContext(request))
'''
  La vista ver_unico_cod: Muestra un codigo de barras y su imagen en base a su codigo 
'''
def ver_unico_cod(request,id_cofre):
	cofre = CodigoBarras.objects.get(codigo=id_cofre)
	ctx = {'cofre':cofre}
	return render_to_response('inventario/muestraProducto.html',ctx,context_instance = RequestContext(request))

        
