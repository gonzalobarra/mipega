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
	messages.success(request, 'plugin de mensajes final final.')
	form = BuscaRapidaForm(request.POST or None)
	localidades = Localidad.objects.all()
	cargos = Cargo.objects.all()
	ctx ={'form_busqueda_rapida':form, 'localidades':localidades, 'cargos':cargos}
	return render_to_response('MP/index.html',ctx,context_instance=RequestContext(request))

def detalle_socio_view(request, id_socio):
	socios = Socio.objects.all()

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
			element = {'id':socio.id, 'titulo':socio.usuario, 'descripcion':str_coment}
			resultados_busqueda.append(element)
		ctx = {'resultados_busqueda': resultados_busqueda, 'cant_resultados':len(resultados_busqueda),'mensaje':mensaje}
		return render_to_response('MP/resultados.html',ctx,context_instance=RequestContext(request))
	else:
		socios = Socio.objects.all()
		resultados_busqueda = []
		for socio in socios:
			element = {'id':socio.id, 'titulo':socio.usuario, 'descripcion':socio.comentario}
			resultados_busqueda.append(element)
		#resultados_busqueda = [{'id':1,'titulo':"asd", 'descripcion':"loremasd"},{'id':2,'titulo':"asd2", 'descripcion':"loremasd2"}]
		ctx = {'resultados_busqueda': resultados_busqueda, 'cant_resultados':len(resultados_busqueda),'mensaje':mensaje}
		return render_to_response('MP/resultados.html',ctx,context_instance=RequestContext(request))

def pruebita(request):
	form = BuscaRapidaForm(request.POST or None)
	ctx = {'form':form} 
	return render_to_response('MP/pruebita.html',ctx,context_instance=RequestContext(request))

def registro_view(request):
	form_user = UserForm(request.POST or None)
	form_socio = SocioForm(request.POST or None)
	form_sociol = LocalidadconSocioForm(request.POST or None)
	form_estudio = EstudioForm(request.POST or None)
	form_estudio2 = EstudioForm(request.POST or None)
	form_explab = ExperienciaLaboralForm(request.POST or None)
	form_hab = OtrasHabilidadesForm(request.POST or None)

	if request.POST:
		if form_user.is_valid():
			try:
				clave = form_user.cleaned_data['password']
				usuario = User.objects.create_user(form_user.cleaned_data['username'], form_user.cleaned_data['email'], clave)
				usuario.save()
				usuario_inst = User.objects.get(username = form_user.cleaned_data['username']) 
				nombre_usuario = form_user.cleaned_data['username']
			except:
				print "El usuario ya existe"
			else:
				if form_socio.is_valid():
					try:
						socio = Socio(usuario=form_socio.cleaned_data['usuario'], comentario=form_socio.cleaned_data['comentario'], nacionalidad=form_socio.cleaned_data['nacionalidad'],telefono=form_socio.cleaned_data['telefono'], web=form_socio.cleaned_data['web'], ano_nacimiento=form_socio.cleaned_data['ano_nacimiento'], sexo=form_socio.cleaned_data['sexo'], tiene_hijos=form_socio.cleaned_data['tiene_hijos'], estado_civil=form_socio.cleaned_data['estado_civil'], pretencion_renta=form_socio.cleaned_data['pretencion_renta'], tipo_contrato=form_socio.cleaned_data['tipo_contrato'], user=usuario_inst) 
						socio.save()
						socio_inst = Socio.objects.get(user__username = nombre_usuario)
					except:
						print "El socio ya existe"
						usuario.delete()
					else:
						if form_sociol.is_valid():
							localidad = LocalidadConSocio(socio=socio_inst, localidad=form_sociol.cleaned_data['localidad'])
							if form_estudio.is_valid():
								estudio1 = Estudios(estado=form_estudio.cleaned_data['estado'], titulo=form_estudio.cleaned_data['titulo'], institucion=form_estudio.cleaned_data['institucion'], socio=socio_inst)
								if form_estudio2.is_valid():
									estudio2 = Estudios(estado=form_estudio2.cleaned_data['estado'], titulo=form_estudio2.cleaned_data['titulo'], institucion=form_estudio2.cleaned_data['institucion'], socio=socio_inst)
									if form_explab.is_valid():
										explab = ExperienciaLaboral(ano_ingreso=form_explab.cleaned_data['ano_ingreso'], ano_egreso=form_explab.cleaned_data['ano_egreso'], cargo=form_explab.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab.cleaned_data['rubro'])
										if form_hab.is_valid() and explab.ano_ingreso < explab.ano_egreso:
											habilidades = OtrasHabilidades(nivel=form_hab.cleaned_data['nivel'], socio=socio_inst, habilidad=form_hab.cleaned_data['habilidad'])		
											localidad.save()
											estudio1.save()
											estudio2.save()
											explab.save()
											habilidades.save()
											return HttpResponseRedirect('/')

	else:	
		ctx = {'form_user': form_user, 'form_socio':form_socio, 'form_sociol':form_sociol, 'form_estudio':form_estudio, 'form_estudio2': form_estudio2, 'form_explab': form_explab, 'form_hab': form_hab}
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
                return HttpResponseRedirect('/perfil/')
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

def editarperfil_view(request):
	user = request.user.username
	socio = Socio.objects.get(user__username = user)
	localidad = LocalidadConSocio.objects.get(socio__id = socio.id)
	estudios = Estudios.objects.filter(socio__id = socio.id)
	explab = ExperienciaLaboral.objects.get(socio__id = socio.id)
	habilidades = OtrasHabilidades.objects.get(socio__id = socio.id)

	if request.method == 'POST':
		form_socio = SocioForm(request.POST,request.FILES, instance=socio)
		form_sociol = LocalidadconSocioForm(request.POST, request.FILES, instance=localidad.localidad)
		form_estudio1 = EstudioForm(request.POST, request.FILES, instance=estudios[0])
		form_estudio2 = EstudioForm(request.POST, request.FILES, instance=estudios[1])
		form_explab = ExperienciaLaboralForm(request.POST, request.FILES, instance=explab)
		form_hab = OtrasHabilidadesForm(request.POST, request.FILES, instance=habilidades.habilidad)
		if form_socio.is_valid() and form_sociol.is_valid() and form_estudio1.is_valid() and form_estudio2.is_valid() and form_explab.is_valid() and form_hab.is_valid():
			form_socio.save()
			form_estudio1.save()
			form_estudio2.save()
			form_explab.save()
			form_hab.save()
			return HttpResponseRedirect('/editarperfil/')
	else:
		form_socio = SocioForm(instance=socio)
		form_sociol = LocalidadconSocioForm(instance=localidad)
		form_estudio1 = EstudioForm(instance=estudios[0])
		form_estudio2 = EstudioForm(instance=estudios[1])
		form_explab = ExperienciaLaboralForm(instance=explab)
		form_hab = OtrasHabilidadesForm(instance=habilidades)

	ctx = {'form_socio':form_socio, 'form_sociol':form_sociol, 'form_estudio1':form_estudio1,'form_estudio2':form_estudio2, 'form_explab':form_explab, 'form_hab':form_hab}	
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