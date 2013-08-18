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

def index_view(request):
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
		form_user.save()
		form_socio.user = form_user
		if form_socio.is_valid():
			form_socio.save()
			form_sociol.socio = form_socio
			form_estudio.socio = form_socio
			form_estudio2.socio = form_socio
			form_explab.socio = form_socio
			form_hab.socio = form_socio
			form_sociol.save()
			form_estudio.save()
			form_estudio2.save()
			form_explab.save()
			form_hab.save()

		return HttpResponseRedirect('/')

	ctx = {'form_user':form_user, 'form_socio': form_socio, 'form_sociol': form_sociol, 'form_estudio': form_estudio, 'form_estudio2': form_estudio2, 'form_explab': form_explab, 'form_hab': form_hab}

	return render_to_response('MP/registro.html', ctx, context_instance=RequestContext(request))