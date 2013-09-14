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

def index_view(request):
	messages.success(request, 'plugin de mensajes final final.')
	form = BuscaRapidaForm(request.POST or None)
	localidades = Localidad.objects.all()
	cargos = Cargo.objects.all()
	ctx ={'form_busqueda_rapida':form, 'localidades':localidades, 'cargos':cargos}
	return render_to_response('MP/index.html',ctx,context_instance=RequestContext(request))

def busqueda_rapida_view(request):
	form = BuscaRapidaForm(request.POST or None)
	#falta implementar aqui la busqueda rapida, ya llegan los valores del form
	if request.method == "POST":
		#mensaje = form.is_valid()
		cargo = request.POST['cargo']
		edad  = request.POST['edad']
		sexo  = request.POST['optionsRadios']
		localidad = request.POST['localidad']

		ides = []

		socios = Socio.objects.all()


		resultados_busqueda = [{'titulo':"asd", 'descripcion':"loremasd"},{'titulo':"asd2", 'descripcion':"loremasd2"}]
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

	if request.POST and form_user.is_valid():
		clave = form_user.cleaned_data['password']
		clave_rep = form_user.cleaned_data['ClaveRepetida']
		if clave == clave_rep:
			usuario = User.objects.create_user(form_user.cleaned_data['username'], form_user.cleaned_data['email'], clave)
			usuario.save()
			usuario_inst = User.objects.get(username = form_user.cleaned_data['username']) 
			nombre_usuario = form_user.cleaned_data['username']
			if form_socio.is_valid():
				socio = Socio(usuario=form_socio.cleaned_data['usuario'],telefono=form_socio.cleaned_data['telefono'], web=form_socio.cleaned_data['web'], ano_nacimiento=form_socio.cleaned_data['ano_nacimiento'], sexo=form_socio.cleaned_data['sexo'], tiene_hijos=form_socio.cleaned_data['tiene_hijos'], estado_civil=form_socio.cleaned_data['estado_civil'], pretencion_renta=form_socio.cleaned_data['pretencion_renta'], tipo_contrato=form_socio.cleaned_data['tipo_contrato'], nacionalidad=form_socio.cleaned_data['nacionalidad'], comentario=form_socio.cleaned_data['comentario'] ,user=usuario_inst) 
				socio.save()
				socio_inst = Socio.objects.get(user__username = nombre_usuario)
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
		ctx = {'form_user':form_user, 'form_socio': form_socio, 'form_sociol': form_sociol, 'form_estudio': form_estudio, 'form_estudio2': form_estudio2, 'form_explab': form_explab, 'form_hab': form_hab}
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
                return HttpResponseRedirect('/')
            else:
                # Mensaje warning
                messages.warning(request, 'Tu cuenta ha sido desactivada.')
                return HttpResponseRedirect('/')
        else:
            # Mensaje de errorreturn HttpResponseRedirect('/')
            messages.error(request, 'Nombre de usuario o password erronea.')
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        ctx = {'form':form}
        return render_to_response('MP/login.html',ctx,context_instance=RequestContext(request))
 
#@login_required(login_url='/serco')
def logout_view(request):
    """
    Cierra la sesion de un usuario y lo redirecciona al home
    """
    logout(request)
    return HttpResponseRedirect('/')

def editarPerfil_view(request):
    return HttpResponseRedirect('/')



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