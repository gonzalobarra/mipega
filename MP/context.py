from django.contrib.auth.models import User
from MP.models import  Socio, Mensaje


def datos_globales(request):
	if not request.user.is_anonymous():
		socio = Socio.objects.get(user = request.user)
		nombre = socio.nombre
		cantidad_mensajes = len(Mensaje.objects.filter(socio=socio).filter(leido=False))
		dict = {
			'NOMBRE_USUARIO':nombre,
			'CANTIDAD_MENSAJES':cantidad_mensajes
		}
		return dict
	else:
		return {}