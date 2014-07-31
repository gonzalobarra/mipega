# -*- coding: Utf8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.core.mail import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from MP.forms import *
from django.contrib.auth.models import User
from MP.models import *
from MP.urls import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import *
from dateutil.relativedelta import *
from django.core.urlresolvers import reverse
from django.utils import timezone
import json

def digito_verificador(rut):
	separado = rut.split('-')
	value = 11 - sum([ int(a)*int(b)  for a,b in zip(str(separado[0]).zfill(8), '32765432')])%11
	digito = {10: 'K', 10: 'k', 11: '0'}.get(value, str(value))
	if separado[1] == digito:
		return True
	else:
		return False	

def cleaner(string):
	#Se eliminan los espacios iniciales y finales del string en caso de tenerlos
	sin_espacios = string.strip()
	#Se corta el string para obtener la primera palabra y luego se capitaliza
	lista = sin_espacios.split()
	if len(lista) > 1:
		listo = ""
		lista[0] = lista[0].capitalize()
		for elemento in lista:
			listo = listo.strip() + " " + elemento
		return listo
	else:
		if len(lista) == 1:
			return lista[0].capitalize()
		if len(lista) == 0:
			return None		


def traspasoCargoE(socio):
	if socio.cargo_extra != None:
		cargos_nuevos = socio.cargo_extra
		lista_cargos = cargos_nuevos.split(',')
		if len(lista_cargos) > 0:
			for cargo in lista_cargos:
				limpio = cleaner(cargo)
				if limpio != None:
					test = Cargo.objects.filter(nombre=limpio)
					if len(test) == 0:
						#Se crea el cargo nuevo y luego se hace la relación con el socio, finalmente se debe eliminar cargo_extra de socio
						cargo_nuevo = Cargo(nombre=limpio)
						cargo_nuevo.save()
						empleo_nuevo = EmpleoBuscado(socio=socio, cargo=cargo_nuevo)
						empleo_nuevo.save()
			socio.cargo_extra = None
			socio.save()				

def index_view(request):
	form = BuscaRapidaForm(request.POST or None)
	localidades = Localidad.objects.all()
	cargos = Cargo.objects.all()
	ctx ={'form_busqueda_rapida':form,'localidades':localidades, 'cargos':cargos, "wololo":RequestContext(request)}
	return render_to_response('MP/index.html',ctx,context_instance=RequestContext(request))

def login_view(request):
	"""
	Vista encargada autenticar un usuario para ingresar al sistema
	"""
	if not request.user.is_anonymous():
	    return HttpResponseRedirect('/')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				# redireccionar al inicio
				socio = Socio.objects.filter(user = user)
				if len(socio)==1:
					messages.success(request, 'Bienvenido ' + socio[0].nombre)
				else:
					messages.success(request, 'Bienvenido Admin')

				return HttpResponseRedirect('/')
			else:
				# Mensaje warning
				messages.warning(request, 'Tu cuenta ha sido desactivada.')
				return HttpResponseRedirect('/')
		else:
			# Mensaje de errorreturn HttpResponseRedirect('/')
			messages.error(request, 'Nombre de usuario o password erronea.')
			form = BuscaRapidaForm(request.POST or None)
			localidades = Localidad.objects.all()
			cargos = Cargo.objects.all()
			ctx ={'form_busqueda_rapida':form,'localidades':localidades, 'cargos':cargos}
			return render_to_response('MP/index.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def detalle_socio_folio_view(request):
	if request.method == "POST":
		if "folio" in request.POST:
			socio = Socio.objects.filter(folio =request.POST['folio'])
			if len(socio) == 1:
				return detalle_socio_view(request, socio[0].id)
			else:
				messages.warning(request, "Folio incorrecto.")
				return HttpResponseRedirect("/")

	return HttpResponseRedirect("/")

def detalle_socio_view(request, id_socio):
	socio = Socio.objects.get(pk =id_socio)
	edad = socio.edad
	#datetime.datetime.today().year - int(socio.ano_nacimiento)
	localidades = Localidad.objects.filter(id__in = LocalidadConSocio.objects.filter(socio = socio).values_list('localidad',flat=True))
	cargos = Cargo.objects.filter(id__in=EmpleoBuscado.objects.filter(socio = socio).values_list('cargo',flat=True))
	estudios_escolares = Estudios.objects.filter(socio = socio).filter(titulo__tipo = "t").exclude(estado=None)
	estudios_superiores = Estudios.objects.filter(socio = socio).exclude(titulo__tipo = "t").exclude(estado=None).exclude(titulo=None)
	habilidades = OtrasHabilidades.objects.filter(socio=socio).exclude(habilidad=None)
	experiencia = ExperienciaLaboral.objects.filter(socio=socio).exclude(cargo=None).exclude(rubro=None).exclude(desde=None)
	if estudios_escolares or estudios_superiores or socio.comentario_est :
		estudios = True
	else:
		estudios = False
	ctx = {'socio': socio, 'edad':edad, 'localidades':localidades, 
			'cargos':cargos, 'estudios_superiores':estudios_superiores, 
			'estudios_escolares':estudios_escolares, 'estudios':estudios,
			'experiencia':experiencia, 'habilidades':habilidades}
	return render_to_response('MP/detalle.html',ctx,context_instance=RequestContext(request))

def resultados_view(request):
	if request.method == "POST":
		return render_to_response('MP/resultados_todos.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/busqueda/avanzada")

def infopago_view(request):
	return render_to_response('MP/infopago.html',context_instance=RequestContext(request))

def busqueda_view(request):
	mensaje = ""
	if request.method == "POST":
		socios = Socio.objects.filter(activo=0)
		if "cargo" in request.POST:
			ids_cargos = request.POST.getlist('cargo')
			id_socios_en_cargo = EmpleoBuscado.objects.filter(cargo_id__in=ids_cargos).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_cargo)
		if "otras-habilidades" in request.POST:
			otrasHab = request.POST.getlist('otras-habilidades')
			id_socios_en_otrasHab = OtrasHabilidades.objects.filter(habilidad_id__in=otrasHab).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_otrasHab)
		if "localidad" in request.POST:
			ids_localidades = request.POST.getlist('localidad')
			id_socios_en_localidad = LocalidadConSocio.objects.filter(localidad_id__in=ids_localidades).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_localidad)
		if "estado-civil" in request.POST:
			if request.POST['estado-civil']!="0":
				socios = socios.filter(estado_civil=str(request.POST['estado-civil']))
		if "hijos" in request.POST:
			if request.POST['hijos']!="0":
				socios = socios.filter(tiene_hijos=str(request.POST['hijos']))
		if "contrato" in request.POST:
			if request.POST['contrato']!="0":
				socios = socios.filter(tipo_contrato=str(request.POST['contrato']))

		if "renta" in request.POST:
			if request.POST['renta']!="-":
				socios = socios.filter(pretencion_renta=str(request.POST['renta']))
		if "rubro" in request.POST:
			ids_rubros = request.POST.getlist('rubro')
			id_socios_en_rubro = ExperienciaLaboral.objects.filter(rubro_id__in=ids_rubros).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_rubro)

		if ('carrera1' in request.POST) and ('institucion1' in request.POST):
			if request.POST['carrera1']!="-":
				if request.POST['institucion1']== "-":
					id_carrera = str(request.POST["carrera1"])
					id_socios_en_carrera = Estudios.objects.filter(titulo_id=id_carrera).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_carrera)
				else:
					id_carrera = str(request.POST["carrera1"])
					id_institucion = str(request.POST["institucion1"])
					id_socios_en_carrera = Estudios.objects.filter(titulo_id=id_carrera).filter(institucion_id=id_institucion).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_carrera)
			else:
				if request.POST['institucion1']!="-":
					id_institucion = str(request.POST["institucion1"])
					id_socios_en_institucion = Estudios.objects.filter(institucion_id=id_institucion).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_institucion)
		if 'carrera2' in request.POST and 'institucion2' in request.POST:
			if request.POST['carrera2']!="-":
				if request.POST['institucion2']=="-":
					id_carrera = str(request.POST["carrera2"])
					id_socios_en_carrera = Estudios.objects.filter(titulo_id=id_carrera).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_carrera)
				else:
					id_carrera = str(request.POST["carrera2"])
					id_institucion = str(request.POST["institucion2"])
					id_socios_en_carrera = Estudios.objects.filter(titulo_id=id_carrera).filter(institucion_id=id_institucion).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_carrera)
			else:
				if request.POST['institucion2']!="-":
					id_institucion = str(request.POST["institucion2"])
					id_socios_en_institucion = Estudios.objects.filter(institucion_id=id_institucion).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_institucion)	
		if 'edad' in request.POST:
			edad  = request.POST['edad']
			menor = int(edad.split(',')[0])
			mayor = int(edad.split(',')[1])
			socios = socios.exclude(edad__lt=menor)
			socios = socios.exclude(edad__gt=mayor)
			if menor!=18 or mayor != 100:
				socios = socios.exclude(edad = None)
		if 'optionsRadios' in request.POST:
			sexo  = request.POST['optionsRadios']
			if sexo != "i":
				socios = socios.filter(sexo=sexo)
		#FIN DE LOS FILTROS
		cantidad_resultados= len(socios)
		resultados_busqueda = []
		for socio in socios:
			if len(resultados_busqueda) <10:
				str_coment = str(socio.nombre)+ ": año nacimiento - " + str(socio.edad) + " estado civil:~"+ str(socio.estado_civil)+"~"
				element = {'id':socio.id, 'folio':socio.folio, 'nombre':socio.nombre,'descripcion':str_coment}
				resultados_busqueda.append(element)
		ctx = {'resultados_busqueda': resultados_busqueda, 'cant_resultados':cantidad_resultados,'mensaje':mensaje}
		return render_to_response('MP/resultados.html',ctx,context_instance=RequestContext(request))
	else:
		if 'cargo' in request.GET:
			ant_cargos = request.GET.getlist('cargo')
			aux = ant_cargos
			ant_cargos = []
			for x in aux:
				ant_cargos.append(int(x))
		else: 
			ant_cargos = []
		if 'edad' in request.GET:
			ant_edad = request.GET['edad']
		else:
			ant_edad = "18,100"
		if 'optionsRadios' in request.GET:
			ant_option = request.GET['optionsRadios']
		else:
			ant_option = "-"
		if 'localidad' in request.GET:
			ant_localidades = request.GET.getlist('localidad')
			aux = ant_localidades
			ant_localidades = []
			for x in aux:
				ant_localidades.append(int(x))
		else:
			ant_localidades = []
		form = BuscaRapidaForm(request.POST or None)
		localidades = Localidad.objects.all()
		cargos = Cargo.objects.all()
		rubros = Rubro.objects.all()
		carreras_escolares = Titulo.objects.filter(tipo='t')
		carreras_superiores = Titulo.objects.exclude(tipo='t')
		instituciones_escolares = Institucion.objects.filter(colegio=True)
		instituciones_superiores = Institucion.objects.filter(colegio=False)
		tipoHabilidades = TipoHabilidad.objects.all().order_by('-nombre')
		habilidades = Habilidad.objects.all()
		ctx ={'form_busqueda_rapida':form, 'localidades':localidades, 'cargos':cargos,'rubros':rubros,
			  'carreras_escolares':carreras_escolares, 'carreras_superiores':carreras_superiores,
			  'instituciones_escolares':instituciones_escolares, 'instituciones_superiores':instituciones_superiores,
			  'tipoHabilidades':tipoHabilidades, 'habilidades':habilidades,'ant_localidades':ant_localidades,
			  'ant_cargos':ant_cargos,'ant_edad':ant_edad, 'ant_option':ant_option}
		return render_to_response('MP/busqueda.html',ctx,context_instance=RequestContext(request))

def enviar_mensaje_view(request):
	#enviar mendaje
	nombre = request.POST['nombre']
	contacto = request.POST['contacto']
	mensaje = request.POST['mensaje']
	socio = Socio.objects.get(pk=request.POST['id_user'])
	correo = socio.user.email
	#Esto no está funcionando por que no se conoce el correo del usuario que esta en la tabla user
	#usuario = User.objects.get(id=request.POST['id_user']+1)
	now = datetime.now()
	if nombre!="" and contacto!="" and mensaje!="":
		#Envia correo electronico
		asunto = "Mipega - Nuevo mensaje de " + nombre
		contenido = "Correo de contacto:" + contacto + "\nMensaje:" + mensaje
		#email = EmailMessage(asunto, contenido,['contacto.workapps@gmail.com'])
		#Actualmente se encuentra con esta configuracion a modo de prueba
		send_mail(asunto, contenido, 'contacto.workapps@gmail.com',[correo], fail_silently=False)
		#Envia mensaje a la bandeja de la aplicacion
		mensaje = Mensaje(fecha=now,contenido=mensaje, nombre_contacto=nombre,medio_contacto=contacto, socio= socio)
		mensaje.save()
		return HttpResponse("enviado")
	return HttpResponse("Debe llenar todos los campos")


def busqueda_rapida_view(request):
	form = BuscaRapidaForm(request.POST or None)
	mensaje = ""
	#falta implementar aqui la busqueda rapida, ya llegan los valores del form
	if request.method == "POST":
		socios = Socio.objects.filter(activo=0)
		if "cargo" in request.POST:
			ids_cargos = request.POST.getlist('cargo')
			id_socios_en_cargo = EmpleoBuscado.objects.filter(cargo_id__in=ids_cargos).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_cargo)
		if "localidad" in request.POST:
			ids_localidades = request.POST.getlist('localidad')
			id_socios_en_localidad = LocalidadConSocio.objects.filter(localidad_id__in=ids_localidades).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_localidad)
		if 'edad' in request.POST:
			edad  = request.POST['edad']
			menor = int(edad.split(',')[0])
			mayor = int(edad.split(',')[1])
			
			socios = socios.exclude(edad__lt=menor)
			socios = socios.exclude(edad__gt=mayor)
			if menor!=18 or mayor != 100:
				socios = socios.exclude(edad = None)
		if 'optionsRadios' in request.POST:
			sexo  = request.POST['optionsRadios']
			if sexo != "i":
				socios = socios.filter(sexo=sexo)
		resultados_busqueda = []
		cant_resultados = len(socios)
		for socio in socios[:10]:
			str_coment = str(socio.nombre)+ ": No se ha detallado la informacion a mostrar- " + str(socio.edad)
			#+ str(edad)
			element = {'id':socio.id, 'folio':socio.folio, 'nombre':socio.nombre,'descripcion':str_coment}
			resultados_busqueda.append(element)
		ctx = {'resultados_busqueda': resultados_busqueda, 'cant_resultados':cant_resultados,'mensaje':mensaje}
		return render_to_response('MP/resultados.html',ctx,context_instance=RequestContext(request))


def resultados_completos(request):
	tam_pagina = 3
	if request.method == "GET":
		if 'page' in request.GET:
			pagina = int(request.GET['page'])
		else:
			pagina = 1
		socios = Socio.objects.filter(activo=0)
		if "cargo" in request.GET:

			ids_cargos = request.GET.getlist('cargo')
			id_socios_en_cargo = EmpleoBuscado.objects.filter(cargo_id__in=ids_cargos).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_cargo)
		if "localidad" in request.GET:
			ids_localidades = request.GET.getlist('localidad')
			id_socios_en_localidad = LocalidadConSocio.objects.filter(localidad_id__in=ids_localidades).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_localidad)
		if "estado-civil" in request.GET:
			if request.GET['estado-civil']!="0":
				socios = socios.filter(estado_civil=str(request.GET['estado-civil']))
		if "hijos" in request.GET:
			if request.GET['hijos']!="0":
				socios = socios.filter(tiene_hijos=str(request.GET['hijos']))
		if "contrato" in request.GET:
			if request.GET['contrato']!="0":
				socios = socios.filter(tipo_contrato=str(request.GET['contrato']))

		if "renta" in request.GET:
			if request.GET['renta']!="-":
				socios = socios.filter(pretencion_renta=str(request.GET['renta']))
		if "rubro" in request.GET:
			ids_rubros = request.GET.getlist('rubro')
			id_socios_en_rubro = ExperienciaLaboral.objects.filter(rubro_id__in=ids_rubros).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_rubro)


		if ('carrera1' in request.GET) and ('institucion1' in request.GET):
			if request.GET['carrera1']!="-":
				if request.GET['institucion1']== "-":
					id_carrera = str(request.GET["carrera1"])
					id_socios_en_carrera = Estudios.objects.filter(titulo_id=id_carrera).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_carrera)
				else:
					id_carrera = str(request.GET["carrera1"])
					id_institucion = str(request.GET["institucion1"])
					id_socios_en_carrera = Estudios.objects.filter(titulo_id=id_carrera).filter(institucion_id=id_institucion).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_carrera)
			else:
				if request.GET['institucion1']!="-":
					id_institucion = str(request.GET["institucion1"])
					id_socios_en_institucion = Estudios.objects.filter(institucion_id=id_institucion).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_institucion)	
		if 'carrera2' in request.GET and 'institucion2' in request.GET:
			if request.GET['carrera2']!="-":
				if request.GET['institucion2']=="-":
					id_carrera = str(request.GET["carrera2"])
					id_socios_en_carrera = Estudios.objects.filter(titulo_id=id_carrera).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_carrera)
				else:
					id_carrera = str(request.GET["carrera2"])
					id_institucion = str(request.GET["institucion2"])
					id_socios_en_carrera = Estudios.objects.filter(titulo_id=id_carrera).filter(institucion_id=id_institucion).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_carrera)
			else:
				if request.GET['institucion2']!="-":
					id_institucion = str(request.GET["institucion2"])
					id_socios_en_institucion = Estudios.objects.filter(institucion_id=id_institucion).values_list('socio_id',flat=True).distinct()
					socios = socios.filter(id__in=id_socios_en_institucion)	
		if 'edad' in request.GET:
			edad  = request.GET['edad']
			menor = int(edad.split(',')[0])
			mayor = int(edad.split(',')[1])
			socios = socios.exclude(edad__lt=menor)
			socios = socios.exclude(edad__gt=mayor)
		if 'optionsRadios' in request.GET:
			sexo  = request.GET['optionsRadios']
			if sexo != "i":
				socios = socios.filter(sexo=sexo)
		#FIN DE LOS FILTROS
		ult = int(len(socios)/tam_pagina)
		if ult*tam_pagina < len(socios):
			ult = 1+ult
		if pagina > ult:
			pagina = 1
		ant = pagina-1
		sig = pagina+1
		if sig > ult:
			sig = ult
		cantidad_resultados= len(socios)
		#socios = socios[0:tam_pagina]

		resultados_busqueda = []
		i = 0
		for socio in socios:
			str_coment = str(socio.nombre)+ ": año nacimiento - " + str(socio.edad) + " estado civil:~"+ str(socio.estado_civil)+"~"
			element = {'id':socio.id, 'folio':socio.folio, 'nombre':socio.nombre,'descripcion':str_coment}
			if i >= (pagina-1)*tam_pagina:
				if len(resultados_busqueda) < tam_pagina:
					resultados_busqueda.append(element)
			i=i+1
		hasta = pagina*tam_pagina
		if hasta > cantidad_resultados:
			hasta = cantidad_resultados
		ctx = {'resultados_busqueda': resultados_busqueda, 'cant_resultados':cantidad_resultados,'desde':(pagina-1)*tam_pagina+1,'hasta':hasta,'sig':sig,'ant':ant, 'actual':pagina, 'ult':ult, 'rango':range(ult+1)}
		return render_to_response('MP/resultados_completos.html',ctx,context_instance=RequestContext(request))



def pruebita(request):
	user = request.user.username
	socio = Socio.objects.get(user__username = user)
	estudios = Estudios.objects.filter(socio__id = socio.id)
	habilidades = OtrasHabilidades.objects.filter(socio__id = socio.id)
	experiencialab = ExperienciaLaboral.objects.filter(socio__id=socio.id)
	lista = []
	for estudio in estudios:
		lista.append(estudio)

	ctx = {'estudios':estudios, 'lista':lista, 'experiencialab': experiencialab, 'est1':estudios[0], 'est2':estudios[1], 'est3':estudios[2]} 
	return render_to_response('MP/pruebita.html',ctx,context_instance=RequestContext(request))

def registro_view(request):

	form_user = UserForm(request.POST or None) #Agregada
	form_socio = SocioForm(request.POST or None) #Agregada
	form_estudio = EstudioForm(request.POST or None, prefix='est1') #Escolar
	form_estudio.fields["institucion"].queryset = Institucion.objects.filter(colegio=True)
	form_estudio.fields["titulo"].queryset = Titulo.objects.filter(tipo="t")
	form_estudio2 = EstudioForm(request.POST or None, prefix='est2') #Superior
	form_estudio2.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
	form_estudio2.fields["titulo"].queryset = Titulo.objects.exclude(tipo='t')
	form_estudio3 = EstudioForm(request.POST or None, prefix='est3') #Superior
	form_estudio3.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
	form_estudio3.fields["titulo"].queryset = Titulo.objects.exclude(tipo='t')
	form_explab = ExperienciaLaboralForm(request.POST or None, prefix='esp1')
	form_explab2 = ExperienciaLaboralForm(request.POST or None, prefix='esp2')
	form_explab3 = ExperienciaLaboralForm(request.POST or None, prefix='esp3')
	form_explab4 = ExperienciaLaboralForm(request.POST or None, prefix='esp4')
	form_hab = OtrasHabilidadesForm(request.POST or None, prefix='hab1')
	form_hab.fields["habilidad"].queryset = Habilidad.objects.filter(tipoHabilidad__nombre='Deporte')
	form_hab2 = OtrasHabilidadesForm(request.POST or None, prefix='hab2')
	form_hab2.fields["habilidad"].queryset = Habilidad.objects.filter(tipoHabilidad__nombre='Idioma')
	

	cargos = Cargo.objects.all()
	localidades = Localidad.objects.all()
	if request.POST:
		if form_user.is_valid():
			
			clave = form_user.cleaned_data['password']
			clave2 = form_user.cleaned_data['ClaveRepetida']
			if clave == clave2:
				# Agregar la condicion de que el correo no puede ser vacio
				if form_user.cleaned_data['username'] == '' or form_user.cleaned_data['username'] == None or clave == '' or clave == None or form_user.cleaned_data['email'] == '' or form_user.cleaned_data['email'] == None or digito_verificador(form_user.cleaned_data['username']) == False:
					messages.warning(request, "El nombre de usuario, clave y email no pueden ser nulos")
					HttpResponseRedirect('/registro')
				else:
					usuario = User.objects.create_user(form_user.cleaned_data['username'], form_user.cleaned_data['email'],clave)
					usuario.save()
			else:
				messages.warning(request,"Las claves ingresadas no coinciden")
				return HttpResponseRedirect('/registro')		
		
			if form_socio.is_valid() and form_user.is_valid():
				usuario_inst = User.objects.get(username = form_user.cleaned_data['username'])
				try:
					foliox = (hex(usuario_inst.id + 10555665)).split('0x')[1]
					if form_socio.cleaned_data['nombre'] != "":
						socio = Socio(user=usuario_inst,nacionalidad=form_socio.cleaned_data['nacionalidad'],nombre=form_socio.cleaned_data['nombre'],telefono=None,web=None,edad=form_socio.cleaned_data['edad'],sexo=form_socio.cleaned_data['sexo'],tiene_hijos=form_socio.cleaned_data['tiene_hijos'],estado_civil=form_socio.cleaned_data['estado_civil'], pretencion_renta=form_socio.cleaned_data['pretencion_renta'], tipo_contrato=form_socio.cleaned_data['tipo_contrato'], comentario_est=form_socio.cleaned_data['comentario_est'],folio=foliox,magister=form_socio.cleaned_data['magister'],disponibilidad=form_socio.cleaned_data['disponibilidad'],disponibilidadV=form_socio.cleaned_data['disponibilidadV'],cargo_extra=form_socio.cleaned_data['cargo_extra'],doctorado=form_socio.cleaned_data['doctorado'])
						socio.save()
					else:
						messages.warning(request,"El nombre de usuario no puede ser vacio")
						return HttpResponseRedirect('/registro')	
				except:
					#Revisar acá esta condición que no se está cumpliendo en ocaciones
					messages.warning(request, "Error al crear el socio")
					usuario_inst.delete()
					return HttpResponseRedirect('/registro')
				#De aca para abajo van los forms que no necesitan comprobaciones.
				#Ojo con los cargos y localidades si no se ingresa nada, revisar despues.
				else:
					socio_inst = Socio.objects.get(user=usuario_inst)
					#Cargos buscados
					if "cargo" in request.POST:
						ids_cargos = request.POST.getlist('cargo')
						for cargo in ids_cargos:
							cargo_socio = Cargo.objects.get(id=cargo)
							asig_cargo = EmpleoBuscado(socio=socio_inst,cargo=cargo_socio)
							asig_cargo.save()
					#Localidad dondes se busca el trabajo
					if "localidad" in request.POST:
						ids_localidades = request.POST.getlist('localidad')
						for localidad in ids_localidades:
							localidad_socio = Localidad.objects.get(id=localidad)
							asig_localidad = LocalidadConSocio(socio=socio_inst,localidad=localidad_socio)
							asig_localidad.save() 
					
					#Estudios
					if form_estudio.is_valid():
						estudio1 = Estudios(estado=form_estudio.cleaned_data['estado'], titulo=form_estudio.cleaned_data['titulo'], institucion=form_estudio.cleaned_data['institucion'], socio=socio_inst)
						estudio1.save()
					if form_estudio2.is_valid():
						estudio2 = Estudios(estado=form_estudio2.cleaned_data['estado'], titulo=form_estudio2.cleaned_data['titulo'], institucion=form_estudio2.cleaned_data['institucion'], socio=socio_inst)
						estudio2.save()
					if form_estudio3.is_valid():
						estudio3 = Estudios(estado=form_estudio3.cleaned_data['estado'], titulo=form_estudio3.cleaned_data['titulo'], institucion=form_estudio3.cleaned_data['institucion'], socio=socio_inst)
						estudio3.save()
					
					#Experiencia laboral
					if form_explab.is_valid():
						explab = ExperienciaLaboral(desde=form_explab.cleaned_data['desde'], hasta=form_explab.cleaned_data['hasta'], comentario=form_explab.cleaned_data['comentario'], cargo=form_explab.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab.cleaned_data['rubro'])
						explab.save()
					if form_explab2.is_valid():
						explab2= ExperienciaLaboral(desde=form_explab2.cleaned_data['desde'], hasta=form_explab.cleaned_data['hasta'], comentario=form_explab2.cleaned_data['comentario'], cargo=form_explab2.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab2.cleaned_data['rubro'])
						explab2.save()
					if form_explab3.is_valid():
						explab3 = ExperienciaLaboral(desde=form_explab3.cleaned_data['desde'], hasta=form_explab.cleaned_data['hasta'], comentario=form_explab3.cleaned_data['comentario'], cargo=form_explab3.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab3.cleaned_data['rubro'])
						explab3.save()
					if form_explab4.is_valid():
						explab4 = ExperienciaLaboral(desde=form_explab4.cleaned_data['desde'], hasta=form_explab.cleaned_data['hasta'], comentario=form_explab4.cleaned_data['comentario'], cargo=form_explab4.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab4.cleaned_data['rubro'])
						explab4.save()
					
					#Otras habilidades
					if form_hab.is_valid():
						habilidades = OtrasHabilidades(nivel=form_hab.cleaned_data['nivel'], socio=socio_inst, habilidad=form_hab.cleaned_data['habilidad'])		
						habilidades.save()
					if form_hab2.is_valid():
						habilidades2 = OtrasHabilidades(nivel=form_hab2.cleaned_data['nivel'], socio=socio_inst, habilidad=form_hab2.cleaned_data['habilidad'])		
						habilidades2.save()
					messages.success(request,"El registro se ha realizado exitosamente")
					#url = reverse('vista_pagoregistro', kwargs={ 'id_socio': socio_inst.id })
					usuario_inst = authenticate(username=form_user.cleaned_data['username'],password=form_user.cleaned_data['password'])
					login(request, usuario_inst)
					return HttpResponseRedirect('/')
		#Else final
		else:
			messages.warning(request,"Error en los datos ingresados")
			return HttpResponseRedirect('/registro')							
	
	ctx = {'form_user': form_user,'form_socio':form_socio,'cargos':cargos, 'localidades':localidades, 'form_estudio':form_estudio,'form_estudio2':form_estudio2,'form_estudio3':form_estudio3, 'form_explab':form_explab, 'form_explab2':form_explab2,'form_explab3':form_explab3, 'form_explab4':form_explab4, 'form_hab':form_hab, 'form_hab2':form_hab2}
	return render_to_response('MP/registro.html', ctx, context_instance=RequestContext(request))

#Pendiente
def pagoregistro_view(request, id_socio):

	pago_form = PagoForm(request.POST or None)


	ctx = {'pago_form': pago_form}

	return render_to_response('MP/pagoexitoso.html',ctx, context_instance=RequestContext(request))


#@login_required(login_url='/')
def logout_view(request):
    """
    Cierra la sesion de un usuario y lo redirecciona al home
    """
    logout(request)
    return HttpResponseRedirect('/')

def perfil_view(request):
    return render_to_response('MP/perfil.html',context_instance=RequestContext(request))

def nuevaclave_view(request):
	if request.method == 'POST':
		user_form = cambiarClave(request.POST)
		if user_form.is_valid():
			pass_user = user_form.cleaned_data['ClaveAntigua']
			if User.check_password(request.user,pass_user):
				pass_nueva = user_form.cleaned_data['ClaveNueva']
				pass_rep= user_form.cleaned_data['ClaveRepetida']
				if pass_nueva==pass_rep:
					User.set_password(request.user,pass_nueva)
					request.user.save()
					messages.success(request, "Su clave ha sido actualizada satisfactoriamente")
				else:
					messages.error(request, "Sus claves no coinciden")	
			return HttpResponseRedirect('/perfil/')

	else:
		user_form = cambiarClave()
	ctx = {'user_form':user_form}
	return render_to_response('MP/nuevaclave.html',ctx, context_instance=RequestContext(request))

#Agregar una funcion que pase los cargos ingresados en cargos extra a la base de datos una vez que se paga exitosamente.
def pagoperfil_view(request):
	if request.method == 'POST':
		pago_form = PagoForm(request.POST)
		if pago_form.is_valid():
			fecha = datetime.now()
			fecha2 = timezone.now()
			socio = Socio.objects.get(user=request.user.id)
			registros = RegistroPago.objects.filter(socio=socio.id)
			#Si el socio no tiene un pago registrado
			if(len(registros)==0):
				if pago_form.cleaned_data['plan'] == '1':
					fecha = fecha + relativedelta(months=+6)
					pago = RegistroPago(socio=socio, fecha_fin=fecha, plan=pago_form.cleaned_data['plan'])
					socio.activo = '0'
					socio.save()
					traspasoCargoE(socio)
					pago.save()
					messages.success(request, 'Pago exitoso')
					return HttpResponseRedirect('/')
				if pago_form.cleaned_data['plan'] == '2':
					fecha = fecha + relativedelta(months=+8)
					pago = RegistroPago(socio=socio, fecha_fin=fecha, plan=pago_form.cleaned_data['plan'])
					pago.save()
					socio.activo = '0'
					socio.save()
					traspasoCargoE(socio)
					messages.success(request, 'Pago exitoso')
					return HttpResponseRedirect('/')
				if pago_form.cleaned_data['plan'] == '3':
					fecha = fecha + relativedelta(months=+12)
					pago = RegistroPago(socio=socio, fecha_fin=fecha, plan=pago_form.cleaned_data['plan'])
					pago.save()
					socio.activo = '0'
					socio.save()
					traspasoCargoE(socio)
					messages.success(request, 'Pago exitoso')
					return HttpResponseRedirect('/')
			#Si el socio tiene pago registrado
			if(len(registros)>0):
				registros2 = RegistroPago.objects.filter(fecha_fin__gt=fecha2).filter(socio=socio.id)
				messages.success(request, registros2[0].fecha_fin)
				#messages.success(request, fecha_final)
				
				#Si el pago esta vencido, se crea uno nuevo
				if(len(registros2)==0):	
					if pago_form.cleaned_data['plan'] == '1':
						fecha = fecha + relativedelta(months=+6)
						pago = RegistroPago(socio=socio, fecha_fin=fecha, plan=pago_form.cleaned_data['plan'])
						socio.activo = '0'
						socio.save()
						pago.save()
						traspasoCargoE(socio)
						messages.success(request, 'Pago exitoso')
						return HttpResponseRedirect('/')
					if pago_form.cleaned_data['plan'] == '2':
						fecha = fecha + relativedelta(months=+8)
						pago = RegistroPago(socio=socio, fecha_fin=fecha, plan=pago_form.cleaned_data['plan'])
						pago.save()
						socio.activo = '0'
						socio.save()
						traspasoCargoE(socio)
						messages.success(request, 'Pago exitoso')
						return HttpResponseRedirect('/')
					if pago_form.cleaned_data['plan'] == '3':
						fecha = fecha + relativedelta(months=+12)
						pago = RegistroPago(socio=socio, fecha_fin=fecha, plan=pago_form.cleaned_data['plan'])
						pago.save()
						socio.activo = '0'
						socio.save()
						traspasoCargoE(socio)
						messages.success(request, 'Pago exitoso')
						return HttpResponseRedirect('/')
				else:
					messages.success(request, 'Su inscripción aun se encuentra activa')
	
	info = {}
	fecha = datetime.now()
	socio = Socio.objects.get(user=request.user.id)
	registros_test = RegistroPago.objects.filter(fecha_fin__gt=fecha).filter(socio=socio.id)
	if len(registros_test) > 0:
		info['validador'] = 1
		info['fecha_fin'] = registros_test[0].fecha_fin
	pago_form = PagoForm()
	ctx = {'pago_form': pago_form, 'info': info}
	return render_to_response('MP/pagarperfil.html', ctx, context_instance=RequestContext(request))	

def listado_view(request):
	socios = Socio.objects.all()
	pagos = RegistroPago.objects.all()
	ctx= {'socios': socios, 'pagos': pagos}
	messages.success(request, socios.count())
	return render_to_response('MP/listapagos.html', ctx, context_instance=RequestContext(request))	

def bandejaentrada_view(request):
	usuario = User.objects.get(username = request.user.username)
	socio = Socio.objects.get(user__id = usuario.id)
	mensajes = Mensaje.objects.filter(socio__id=socio.id)
	ctx = {'mensajes':mensajes} 
	return render_to_response('MP/bandejaentrada.html', ctx, context_instance=RequestContext(request))

def mensaje_view(request, pk):
	mensaje = Mensaje.objects.get(id = pk)
	mensaje.leido = True
	mensaje.save()
	ctx = {'mensaje':mensaje}
	return render_to_response('MP/mensaje.html', ctx, context_instance=RequestContext(request))	

def eliminarmensaje_view(request,pk):
	mensaje = Mensaje.objects.get(id = pk)
	mensaje.delete()
	return render_to_response('MP/bandejaentrada.html',context_instance=RequestContext(request))

def editarperfil_view(request):
	
	user = request.user
	socio = Socio.objects.get(user = user)
	estudios = Estudios.objects.filter(socio = socio)
	habilidades = OtrasHabilidades.objects.filter(socio= socio)
	experienciaslab = ExperienciaLaboral.objects.filter(socio=socio)
	listae = []
	listah = []
	listaex = []
	for habilidad in habilidades:
		listah.append(habilidad)
	for estudio in estudios:
		listae.append(estudio)
	for experiencialab in experienciaslab:
		listaex.append(experiencialab)	
	
	#messages.success(request, listas[0].id)
	#Ver si el socio tiene un pago activo, si es así se llama al funcion encargada de hacer la carga de los nuevos cargos
	hoy = timezone.now()
	value = 0

	registros_pago = RegistroPago.objects.filter(socio=socio).filter(fecha_fin__gt=hoy)
	if len(registros_pago) > 0:
	 		value = 1

	if request.method == 'POST':
		form_socio = SocioForm2(request.POST, request.FILES, instance=socio, prefix='soc')
		form_estudio = EstudioForm(request.POST, request.FILES, instance=listae[0], prefix='est1')
		form_estudio.fields["institucion"].queryset = Institucion.objects.filter(colegio=True)
		form_estudiodos = EstudioForm(request.POST, request.FILES, instance=listae[1], prefix='est2')
		form_estudiodos.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
		form_estudiotres = EstudioForm(request.POST, request.FILES, instance=listae[2], prefix='est3')
		form_estudiotres.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
		form_explab = ExperienciaLaboralForm(request.POST, request.FILES, instance=listaex[0], prefix='exp1')
		form_explab2 = ExperienciaLaboralForm(request.POST, request.FILES, instance=listaex[1], prefix='exp2')
		form_explab3 = ExperienciaLaboralForm(request.POST, request.FILES, instance=listaex[2], prefix='exp3')
		form_explab4 = ExperienciaLaboralForm(request.POST, request.FILES, instance=listaex[3], prefix='exp4')
		form_hab = OtrasHabilidadesForm(request.POST, request.FILES, instance=listah[0], prefix='hab1')
		form_hab.fields["habilidad"].queryset = Habilidad.objects.filter(tipoHabilidad__nombre='Deporte')
		form_hab2 = OtrasHabilidadesForm(request.POST, request.FILES, instance=listah[1], prefix='hab2')
		form_hab2.fields["habilidad"].queryset = Habilidad.objects.filter(tipoHabilidad__nombre='Idioma')

		if form_socio.is_valid():
			form_socio.save()
			if value == 1:
			 	socio = Socio.objects.get(user=request.user.id)
			 	traspasoCargoE(socio)
		if form_estudio.is_valid():
			form_estudio.save()
		if form_estudiodos.is_valid():
			form_estudiodos.save()
		if form_estudiotres.is_valid():
			form_estudiotres.save()
		if form_explab.is_valid():
			form_explab.save()
		if form_explab2.is_valid():
			form_explab2.save() 
		if form_explab3.is_valid():
			form_explab3.save()
		if form_explab4.is_valid():
			form_explab4.save() 
		if form_hab.is_valid():
			form_hab.save() 
		if form_hab2.is_valid():
			form_hab2.save() 
		
		messages.success(request, "Su perfil ha sido modificado exitosamente")	
		return HttpResponseRedirect('/editarperfil/')
	else:
		form_socio = SocioForm2(instance=socio, prefix='soc')
		form_estudio = EstudioForm(instance=listae[0], prefix='est1')
		form_estudio.fields["institucion"].queryset = Institucion.objects.filter(colegio=True)
		form_estudiodos = EstudioForm(instance=listae[1], prefix='est2')
		form_estudiodos.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
		form_estudiotres = EstudioForm(instance=listae[2], prefix='est3')
		form_estudiotres.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
		form_explab = ExperienciaLaboralForm(instance=listaex[0], prefix='exp1')
		form_explab2 = ExperienciaLaboralForm(instance=listaex[1], prefix='exp2')
		form_explab3 = ExperienciaLaboralForm(instance=listaex[2], prefix='exp3')
		form_explab4 = ExperienciaLaboralForm(instance=listaex[3], prefix='exp4')
		form_hab = OtrasHabilidadesForm(instance=listah[0], prefix='hab1')
		form_hab.fields["habilidad"].queryset = Habilidad.objects.filter(tipoHabilidad__nombre='Deporte')
		form_hab2 = OtrasHabilidadesForm(instance=listah[1], prefix='hab2')
		form_hab2.fields["habilidad"].queryset = Habilidad.objects.filter(tipoHabilidad__nombre='Idioma')

	ctx = {'socio':socio,'form_socio':form_socio, 'form_estudio':form_estudio, 'form_estudio2':form_estudiodos, 'form_estudio3':form_estudiotres, 'form_explab':form_explab, 'form_explab2':form_explab2, 'form_explab3':form_explab3, 'form_explab4':form_explab4, 'form_hab':form_hab , 'form_hab2':form_hab2}	
	
	return render_to_response('MP/editarperfil.html', ctx, context_instance=RequestContext(request))		 
