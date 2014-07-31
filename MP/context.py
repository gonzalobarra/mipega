from django.contrib.auth.models import User
from MP.models import  Socio, Mensaje
from MP.forms import *



def datos_globales(request):
	formLogin = LoginForm(request.POST or None)
	if not request.user.is_anonymous():
		socio = Socio.objects.filter(user = request.user)
		if len(socio) == 1:
			nombre = socio[0].nombre
			cantidad_mensajes = len(Mensaje.objects.filter(socio=socio).filter(leido=False))
			dict = {
				'FORM_LOGIN':formLogin,
				'NOMBRE_USUARIO':nombre,
				'CANTIDAD_MENSAJES':cantidad_mensajes
			}
			return dict
		else:
			nombre = "Admin"
			cantidad_mensajes = 0
			dict = {
				'FORM_LOGIN':formLogin,
				'NOMBRE_USUARIO':nombre,
				'CANTIDAD_MENSAJES':cantidad_mensajes
			}
			return dict
	else:
		return {'FORM_LOGIN':formLogin}