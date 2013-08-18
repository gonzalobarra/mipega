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
	if request.POST and form_user.is_valid():
		form_user.save()

		return HttpResponseRedirect('/')

	ctx = {'form_user':form_user, 'form_socio': form_socio, 'form_sociol': form_sociol}

	return render_to_response('MP/registro.html', ctx, context_instance=RequestContext(request))