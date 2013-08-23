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
	messages.warning(request, "hola perrin kakod")
	messages.error(request, ":O que paso")
	messages.info(request, 'SQL statements were executed.')
	return render_to_response('MP/index.html',context_instance=RequestContext(request))

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
				socio = Socio(usuario=form_socio.cleaned_data['usuario'], telefono=form_socio.cleaned_data['telefono'], web=form_socio.cleaned_data['web'], ano_nacimiento=form_socio.cleaned_data['ano_nacimiento'], sexo=form_socio.cleaned_data['sexo'], tiene_hijos=form_socio.cleaned_data['tiene_hijos'], estado_civil=form_socio.cleaned_data['estado_civil'], pretencion_renta=form_socio.cleaned_data['pretencion_renta'], tipo_contrato=form_socio.cleaned_data['tipo_contrato'], user=usuario_inst) 
				socio.save()
				socio_inst = Socio.objects.get(user__username = nombre_usuario)
				if form_sociol.is_valid():
					localidad = LocalidadConSocio(socio=socio_inst, localidad=form_sociol.cleaned_data['localidad'])
					if form_estudio.is_valid():
						estudio1 = Estudios(ano=form_estudio.cleaned_data['ano'], estado=form_estudio.cleaned_data['estado'], titulo=form_estudio.cleaned_data['titulo'], institucion=form_estudio.cleaned_data['institucion'], socio=socio_inst)
						if form_estudio2.is_valid():
							estudio2 = Estudios(ano=form_estudio2.cleaned_data['ano'], estado=form_estudio2.cleaned_data['estado'], titulo=form_estudio2.cleaned_data['titulo'], institucion=form_estudio2.cleaned_data['institucion'], socio=socio_inst)
							if form_explab.is_valid():
								explab = ExperienciaLaboral(ano_ingreso=form_explab.cleaned_data['ano_ingreso'], ano_egreso=form_explab.cleaned_data['ano_egreso'], cargo=form_explab.cleaned_data['cargo'], socio=socio_inst , rubro=form_explab.cleaned_data['rubro'])
								if form_hab.is_valid() and explab.ano_ingreso < ano_egreso:
									habilidades = OtrasHabilidades(nivel=form_hab.cleaned_data['nivel'], socio=socio_inst, habilidad=form_hab.cleaned_data['habilidad'])		
									#usuario.save()
									#socio.save()
									localidad.save()
									estudio1.save()
									estudio2.save()
									explab.save()
									habilidades.save()
									return HttpResponseRedirect('/')
								else:
									usuario.delete()	
				else:
					usuario.delete()				
			else:
				usuario.delete()						
	else:
		ctx = {'form_user':form_user, 'form_socio': form_socio, 'form_sociol': form_sociol, 'form_estudio': form_estudio, 'form_estudio2': form_estudio2, 'form_explab': form_explab, 'form_hab': form_hab}
		return render_to_response('MP/registro.html', ctx, context_instance=RequestContext(request))