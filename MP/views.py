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
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import datetime

def index_view(request):
	form = BuscaRapidaForm(request.POST or None)
	localidades = Localidad.objects.all()
	cargos = Cargo.objects.all()
	ctx ={'form_busqueda_rapida':form, 'localidades':localidades, 'cargos':cargos}
	return render_to_response('MP/index.html',ctx,context_instance=RequestContext(request))

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
	messages.success(request, "debug")
	messages.warning(request, "debug")
	messages.info(request, "debug")
	messages.error(request, "debug")
	socio = Socio.objects.get(pk =id_socio)
	edad = socio.edad#datetime.datetime.today().year - int(socio.ano_nacimiento)
	localidades = Localidad.objects.filter(id__in = LocalidadConSocio.objects.filter(socio = socio).values_list('localidad',flat=True))
	cargos = Cargo.objects.filter(id__in=EmpleoBuscado.objects.filter(socio = socio).values_list('cargo',flat=True))
	estudios_escolares = Estudios.objects.filter(socio = socio).filter(titulo__tipo = "t")
	estudios_superiores = Estudios.objects.filter(socio = socio).exclude(titulo__tipo = "t")
	habilidades = OtrasHabilidades.objects.filter(socio=socio)
	experiencia = ExperienciaLaboral.objects.filter(socio=socio)
	if estudios_escolares or estudios_superiores:
		estudios = True
	else:
		estudios = False
	ctx = {'socio': socio, 'edad':edad, 'localidades':localidades, 
			'cargos':cargos, 'estudios_superiores':estudios_superiores, 
			'estudios_escolares':estudios_escolares, 'estudios':estudios,
			'experiencia':experiencia, 'habilidades':habilidades}
	return render_to_response('MP/detalle.html',ctx,context_instance=RequestContext(request))

def busqueda_view(request):
	if request.method == "POST":
		form = BuscaRapidaForm(request.POST or None)
		mensaje = ""
		ano_actual = datetime.datetime.now().year
		if request.method == "POST":
			socios = Socio.objects.all()
			if "cargo" in request.POST:
				ids_cargos = request.POST.getlist('cargo')
				id_socios_en_cargo = EmpleoBuscado.objects.filter(cargo_id__in=ids_cargos).values_list('socio_id',flat=True).distinct()
				socios = socios.filter(id__in=id_socios_en_cargo)
			if "localidad" in request.POST:
				ids_localidades = request.POST.getlist('localidad')
				mensaje = ids_localidades
				id_socios_en_localidad = LocalidadConSocio.objects.filter(localidad_id__in=ids_localidades).values_list('socio_id',flat=True).distinct()
				socios = socios.filter(id__in=id_socios_en_localidad)
			if "rubro" in request.POST and False:
				ids_rubros = request.POST.getlist('rubro')
				id_socios_en_rubro = ExperienciaLaboral.objects.filter(rubro_id__in=ids_rubros).values_list('socio_id',flat=True).distinct()
				socios = socios.filter(id__in=id_socios_en_rubro)
			edad  = request.POST['edad']
			menor = 0
			mayor = ano_actual
			if edad == "1":
				menor = ano_actual - 24
				mayor = ano_actual - 18
			if edad == "2":
				menor = ano_actual - 29
				mayor = ano_actual - 24
			if edad == "3":
				menor = ano_actual - 37
				mayor = ano_actual - 30
			if edad == "4":
				menor = ano_actual - 44
				mayor = ano_actual - 37
			if edad == "5":
				menor = ano_actual - ano_actual
				mayor = ano_actual - 44
			socios = socios.exclude(ano_nacimiento__lt=menor)
			socios = socios.exclude(ano_nacimiento__gt=mayor)
			sexo  = request.POST['optionsRadios']
			if sexo != "i":
				socios = socios.filter(sexo=sexo)
			socios = Socio.objects.all()
			hijos  = request.POST['hijos']
			if hijos != "i":
				if(hijos=="1"):
					socios = socios.filter(tiene_hijos="s")
				if(hijos=="0"):
					socios = socios.filter(tiene_hijos="n")
			resultados_busqueda = []
			for socio in socios:
				str_coment = " año nacimiento "+ str(socio.ano_nacimiento)
				element = {'id':socio.id, 'titulo':socio.nombre, 'descripcion':str_coment}
				resultados_busqueda.append(element)
			ctx = {'resultados_busqueda': resultados_busqueda, 'cant_resultados':len(resultados_busqueda),'mensaje':mensaje}
			return render_to_response('MP/resultados.html',ctx,context_instance=RequestContext(request))	
	else:
		form = BuscaRapidaForm(request.POST or None)
		localidades = Localidad.objects.all()
		cargos = Cargo.objects.all()
		rubros = Rubro.objects.all()
		ctx ={'form_busqueda_rapida':form, 'localidades':localidades, 'cargos':cargos,'rubros':rubros}
		return render_to_response('MP/busqueda.html',ctx,context_instance=RequestContext(request))

def enviar_mensaje_view(request):
	#enviar mendaje
	nombre = request.POST['nombre']
	contacto = request.POST['contacto']
	mensaje = request.POST['mensaje']
	socio = Socio.objects.get(pk=request.POST['id_user'])
	now = datetime.datetime.now()
	if nombre!="" and contacto!="" and mensaje!="":
		mensaje = Mensaje(fecha=now, contenido=mensaje, nombre_contacto=nombre,medio_contacto=contacto, socio= socio)
		mensaje.save()
		return HttpResponse("enviado")
	return HttpResponse("Debe llenar todos los campos")


def busqueda_rapida_view(request):
	form = BuscaRapidaForm(request.POST or None)
	mensaje = ""
	ano_actual = datetime.datetime.now().year
	#falta implementar aqui la busqueda rapida, ya llegan los valores del form
	if request.method == "POST":
		socios = Socio.objects.all()
		if "cargo" in request.POST:
			ids_cargos = request.POST.getlist('cargo')
			id_socios_en_cargo = EmpleoBuscado.objects.filter(cargo_id__in=ids_cargos).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_cargo)
		if "localidad" in request.POST:
			ids_localidades = request.POST.getlist('localidad')
			mensaje = ids_localidades
			id_socios_en_localidad = LocalidadConSocio.objects.filter(localidad_id__in=ids_localidades).values_list('socio_id',flat=True).distinct()
			socios = socios.filter(id__in=id_socios_en_localidad)
		edad  = request.POST['edad']
		menor = 0
		mayor = ano_actual
		if edad == "1":
			menor = ano_actual - 24
			mayor = ano_actual - 18
		if edad == "2":
			menor = ano_actual - 29
			mayor = ano_actual - 24
		if edad == "3":
			menor = ano_actual - 37
			mayor = ano_actual - 30
		if edad == "4":
			menor = ano_actual - 44
			mayor = ano_actual - 37
		if edad == "5":
			menor = ano_actual - ano_actual
			mayor = ano_actual - 44
		socios = socios.exclude(ano_nacimiento__lt=menor)
		socios = socios.exclude(ano_nacimiento__gt=mayor)
		sexo  = request.POST['optionsRadios']
		if sexo != "i":
			socios = socios.filter(sexo=sexo)
		resultados_busqueda = []
		for socio in socios:
			str_coment = " año nacimiento "+ str(socio.ano_nacimiento)
			element = {'id':socio.id, 'titulo':socio.nombre, 'descripcion':str_coment}
			resultados_busqueda.append(element)
		ctx = {'resultados_busqueda': resultados_busqueda, 'cant_resultados':len(resultados_busqueda),'mensaje':mensaje}
		return render_to_response('MP/resultados.html',ctx,context_instance=RequestContext(request))

def pruebita(request):
	user = request.user.username
	socio = Socio.objects.get(user__username = user)
	estudios = Estudios.objects.filter(socio__id = socio.id)
	habilidades = OtrasHabilidades.objects.filter(socio__id = socio.id)
	experiencialab = ExperienciaLaboral.objects.filter(socio__id=socio.id)

	ctx = {'estudios':estudios, 'habilidades':habilidades, 'experiencialab': experiencialab, 'est1':estudios[0], 'est2':estudios[1], 'est3':estudios[2]} 
	return render_to_response('MP/pruebita.html',ctx,context_instance=RequestContext(request))

def registro_view(request):

	form_user = UserForm(request.POST or None) #Agregada
	form_socio = SocioForm(request.POST or None) #Agregada
	form_estudio = EstudioForm(request.POST or None, prefix='est1') #Escolar
	form_estudio.fields["institucion"].queryset = Institucion.objects.filter(colegio=True)
	form_estudio2 = EstudioForm(request.POST or None, prefix='est2') #Superior
	form_estudio2.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
	form_estudio3 = EstudioForm(request.POST or None, prefix='est3') #Superior
	form_estudio3.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
	form_explab = ExperienciaLaboralForm(request.POST or None, prefix='esp1')
	form_explab2 = ExperienciaLaboralForm(request.POST or None, prefix='esp2')
	form_explab3 = ExperienciaLaboralForm(request.POST or None, prefix='esp3')
	form_explab4 = ExperienciaLaboralForm(request.POST or None, prefix='esp4')
	form_hab = OtrasHabilidadesForm(request.POST or None, prefix='hab1')
	form_hab2 = OtrasHabilidadesForm(request.POST or None, prefix='hab2')
	form_hab3 = OtrasHabilidadesForm(request.POST or None, prefix='hab3')
	form_hab4 = OtrasHabilidadesForm(request.POST or None, prefix='hab4')

	cargos = Cargo.objects.all()
	localidades = Localidad.objects.all()
	if request.POST:
		if form_user.is_valid():
			try:
				clave = form_user.cleaned_data['password']
				clave2 = form_user.cleaned_data['ClaveRepetida']
				if clave == clave2:
					usuario = User.objects.create_user(form_user.cleaned_data['username'], form_user.cleaned_data['email'],clave)
					usuario.save()
					usuario_inst = User.objects.get(username = form_user.cleaned_data['username']) 
					nombre_usuario = form_user.cleaned_data['username']
				else:
					messages.warning(request,"La clave no coincide")
					return HttpResponseRedirect('/registro')		
			except:
				messages.warning(request,"Error en la información del usuario")
				return HttpResponseRedirect('/registro')
			else:
				if form_socio.is_valid():
					try:
						socio = Socio(user=usuario_inst, nacionalidad=form_socio.cleaned_data['nacionalidad'],nombre=form_socio.cleaned_data['nombre'],telefono=form_socio.cleaned_data['telefono'],web=form_socio.cleaned_data['web'],edad=form_socio.cleaned_data['edad'],sexo=form_socio.cleaned_data['sexo'],tiene_hijos=form_socio.cleaned_data['tiene_hijos'],estado_civil=form_socio.cleaned_data['estado_civil'], pretencion_renta=form_socio.cleaned_data['pretencion_renta'], tipo_contrato=form_socio.cleaned_data['tipo_contrato'], comentario_est=form_socio.cleaned_data['comentario_est'],folio='qwer',magister=form_socio.cleaned_data['magister'],doctorado=form_socio.cleaned_data['doctorado'])
						socio.save()
						socio_inst = Socio.objects.get(user=usuario_inst)
					except:
						messages.warning(request, "Error al crear el socio")
						usuario.delete()
						return HttpResponseRedirect('/registro')
						#Aqui va el tema del cargo.
					else:
						if "cargo" in request.POST:
							ids_cargos = request.POST.getlist('cargo')
							for cargo in ids_cargos:
								cargo_socio = Cargo.objects.get(id=cargo)
								asig_cargo = EmpleoBuscado(socio=socio_inst,cargo=cargo_socio)
								asig_cargo.save()
						#Aqui va el tema de la localidad.
						if "localidad" in request.POST:
							ids_localidades = request.POST.getlist('localidad')
							for localidad in ids_localidades:
								localidad_socio = Localidad.objects.get(id=localidad)
								asig_localidad = LocalidadConSocio(socio=socio_inst,localidad=localidad_socio)
								asig_localidad.save() 
						
						if form_estudio.is_valid():
							estudio1 = Estudios(estado=form_estudio.cleaned_data['estado'], titulo=form_estudio.cleaned_data['titulo'], institucion=form_estudio.cleaned_data['institucion'], socio=socio_inst)
							estudio1.save()
						if form_estudio2.is_valid():
							estudio2 = Estudios(estado=form_estudio2.cleaned_data['estado'], titulo=form_estudio2.cleaned_data['titulo'], institucion=form_estudio2.cleaned_data['institucion'], socio=socio_inst)
							estudio2.save()
						if form_estudio3.is_valid():
							estudio3 = Estudios(estado=form_estudio3.cleaned_data['estado'], titulo=form_estudio3.cleaned_data['titulo'], institucion=form_estudio3.cleaned_data['institucion'], socio=socio_inst)
							estudio3.save()
						
						if form_explab.is_valid():
							explab = ExperienciaLaboral(anos_trabajados=form_explab.cleaned_data['anos_trabajados'], comentario=form_explab.cleaned_data['comentario'], cargo=form_explab.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab.cleaned_data['rubro'])
							explab.save()
						if form_explab2.is_valid():
							explab2= ExperienciaLaboral(anos_trabajados=form_explab2.cleaned_data['anos_trabajados'], comentario=form_explab2.cleaned_data['comentario'], cargo=form_explab2.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab2.cleaned_data['rubro'])
							explab2.save()
						if form_explab3.is_valid():
							explab3 = ExperienciaLaboral(anos_trabajados=form_explab3.cleaned_data['anos_trabajados'], comentario=form_explab3.cleaned_data['comentario'], cargo=form_explab3.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab3.cleaned_data['rubro'])
							explab3.save()
						if form_explab4.is_valid():
							explab4 = ExperienciaLaboral(anos_trabajados=form_explab4.cleaned_data['anos_trabajados'], comentario=form_explab4.cleaned_data['comentario'], cargo=form_explab4.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab4.cleaned_data['rubro'])
							explab4.save()
						
						if form_hab.is_valid():
							habilidades = OtrasHabilidades(nivel=form_hab.cleaned_data['nivel'], socio=socio_inst, habilidad=form_hab.cleaned_data['habilidad'])		
							habilidades.save()
						if form_hab2.is_valid():
							habilidades2 = OtrasHabilidades(nivel=form_hab2.cleaned_data['nivel'], socio=socio_inst, habilidad=form_hab2.cleaned_data['habilidad'])		
							habilidades2.save()
						if form_hab3.is_valid():
							habilidades3 = OtrasHabilidades(nivel=form_hab3.cleaned_data['nivel'], socio=socio_inst, habilidad=form_hab3.cleaned_data['habilidad'])		
							habilidades3.save()
						if form_hab4.is_valid():
							habilidades4 = OtrasHabilidades(nivel=form_hab4.cleaned_data['nivel'], socio=socio_inst, habilidad=form_hab4.cleaned_data['habilidad'])		
							habilidades4.save()
						
						messages.success(request,"El registro se ha realizado exitosamente")
						return HttpResponseRedirect('/')
		#Else final
		else:
			messages.warning(request,"Error en los datos ingresados")
			return HttpResponseRedirect('/registro')							
	else:	
		ctx = {'form_user': form_user,'form_socio':form_socio,'cargos':cargos, 'localidades':localidades, 'form_estudio':form_estudio,'form_estudio2':form_estudio2,'form_estudio3':form_estudio3, 'form_explab':form_explab, 'form_explab2':form_explab2,'form_explab3':form_explab3, 'form_explab4':form_explab4, 'form_hab':form_hab, 'form_hab2':form_hab2, 'form_hab3':form_hab3, 'form_hab4':form_hab4}
		return render_to_response('MP/registro.html', ctx, context_instance=RequestContext(request))

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
                messages.success(request, 'Bienvenido ' + user.username)
                return HttpResponseRedirect('/editarperfil/')
            else:
                # Mensaje warning
                messages.warning(request, 'Tu cuenta ha sido desactivada.')
                return HttpResponseRedirect('/login/')
        else:
            # Mensaje de errorreturn HttpResponseRedirect('/')
            messages.error(request, 'Nombre de usuario o password erronea.')
            return HttpResponseRedirect('/login/')
    else:
        form = LoginForm()
        ctx = {'form':form}
        return render_to_response('MP/login.html',ctx,context_instance=RequestContext(request))
 
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
			return HttpResponseRedirect('/')

	else:
		user_form = cambiarClave()
	ctx = {'user_form':user_form}
	return render_to_response('MP/nuevaclave.html',ctx, context_instance=RequestContext(request))

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
	
	user = request.user.username
	socio = Socio.objects.get(user__username = user)
	estudios = Estudios.objects.filter(socio__id = socio.id)
	habilidades = OtrasHabilidades.objects.filter(socio__id = socio.id)
	experiencialab = ExperienciaLaboral.objects.filter(socio__id=socio.id)
	est1 = estudios[0]
	est2 = estudios[1]
	est3 = estudios[2]
	exp1 = experiencialab[0]
	exp2 = experiencialab[1]
	exp3 = experiencialab[2]
	exp4 = experiencialab[3]
	hab1 = habilidades[0]
	hab2 = habilidades[1]
	hab3 = habilidades[2]
	hab4 = habilidades[3]

	if request.method == 'POST':
		form_socio = SocioForm(request.POST,request.FILES, instance=socio)
		form_estudio = EstudioForm(request.POST, request.FILES, instance=est1, prefix='est1')
		form_estudio.fields["institucion"].queryset = Institucion.objects.filter(colegio=True)
		form_estudiodos = EstudioForm(request.POST, request.FILES, instance=est2, prefix='est2')
		form_estudio.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
		form_estudiotres = EstudioForm(request.POST, request.FILES, instance=est3, prefix='est3')
		form_estudio.fields["institucion"].queryset = Institucion.objects.filter(colegio=False)
		form_explab = ExperienciaLaboralForm(request.POST, request.FILES, instance=exp1, prefix='exp1')
		form_explab2 = ExperienciaLaboralForm(request.POST, request.FILES, instance=exp2, prefix='exp2')
		form_explab3 = ExperienciaLaboralForm(request.POST, request.FILES, instance=exp3, prefix='exp3')
		form_explab4 = ExperienciaLaboralForm(request.POST, request.FILES, instance=exp4, prefix='exp4')
		form_hab = OtrasHabilidadesForm(request.POST, request.FILES, instance=hab1, prefix='hab1')
		form_hab2 = OtrasHabilidadesForm(request.POST, request.FILES, instance=hab2, prefix='hab2')
		form_hab3 = OtrasHabilidadesForm(request.POST, request.FILES, instance=hab3, prefix='hab3')
		form_hab4 = OtrasHabilidadesForm(request.POST, request.FILES, instance=hab4, prefix='hab4')
		if form_socio.is_valid():
			form_socio.save()
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
		if form_hab3.is_valid():
			form_hab3.save()
		if form_hab4.is_valid():
			form_hab4.save()
				
		return HttpResponseRedirect('/editarperfil/')
	else:
		form_socio = SocioForm(instance=socio)
		form_estudio = EstudioForm(instance=est1, prefix='est1')
		form_estudiodos = EstudioForm(instance=est2, prefix='est2')
		form_estudiotres = EstudioForm(instance=est3, prefix='est3')
		form_explab = ExperienciaLaboralForm(instance=exp1, prefix='exp1')
		form_explab2 = ExperienciaLaboralForm(instance=exp2, prefix='exp2')
		form_explab3 = ExperienciaLaboralForm(instance=exp3, prefix='exp3')
		form_explab4 = ExperienciaLaboralForm(instance=exp4, prefix='exp4')
		form_hab = OtrasHabilidadesForm(instance=hab1, prefix='hab1')
		form_hab2 = OtrasHabilidadesForm(instance=hab2, prefix='hab2')
		form_hab3 = OtrasHabilidadesForm(instance=hab3, prefix='hab3')
		form_hab4 = OtrasHabilidadesForm(instance=hab4, prefix='hab4')

	ctx = {'form_socio':form_socio, 'form_estudio':form_estudio, 'form_estudio2':form_estudiodos, 'form_estudio3':form_estudiotres, 'form_explab':form_explab, 'form_explab2':form_explab2, 'form_explab3':form_explab3, 'form_explab4':form_explab4, 'form_hab':form_hab , 'form_hab2':form_hab2 , 'form_hab3':form_hab3, 'form_hab4':form_hab4}	
	
	return render_to_response('MP/editarperfil.html', ctx, context_instance=RequestContext(request))		 

#lineas para poblado parcial de localidades
# def poblarlocalidadcargo(request):
# 	nuevo11 = Localidad(nombre="Angol",tipo="c")
# 	nuevo21 = Localidad(nombre="Antofagasta",tipo="c")
# 	nuevo31 = Localidad(nombre="Antuco",tipo="c")
# 	nuevo51 = Localidad(nombre="Arica",tipo="c")
# 	nuevo11.save()
# 	nuevo21.save()
# 	nuevo31.save()
# 	nuevo51.save()
# 	nuevo1 = Localidad(nombre="PRIMERA REGIÓN DE TARAPACÁ",tipo="r")
# 	nuevo2 = Localidad(nombre="SEGUNDA REGIÓN DE ANTOFAGASTA",tipo="r")
# 	nuevo3 = Localidad(nombre="TERCERA REGIÓN DE ATACAMA",tipo="r")
# 	nuevo5 = Localidad(nombre="METROPOLITANA",tipo="r")
# 	nuevo1.save()
# 	nuevo2.save()
# 	nuevo3.save()
# 	nuevo5.save()
# 	nuevo = Cargo(nombre="Gruero")
# 	nuevo.save()
# 	nuevo1 = Cargo(nombre="Supervisor")
# 	nuevo1.save()
# 	nuevo3 = Cargo(nombre="Jornal")
# 	nuevo3.save()
# 	nuevo4 = Cargo(nombre="Programador")
# 	nuevo4.save()