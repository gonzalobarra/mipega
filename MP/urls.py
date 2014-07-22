from django.conf.urls import patterns, url


urlpatterns = patterns('MP.views',
	url(r'^$','index_view',name='vista_principal'),
	url(r'^registro/$','registro_view',name='vista_registro'),
	url(r'^busqueda/rapida/$','busqueda_rapida_view',name='busqueda_rapida'),
	url(r'^pruebita/$','pruebita',name='pruebita'),
	url(r'^login/$','login_view',name='vista_login'),
	url(r'^logout/$','logout_view',name='vista_logout'),
	url(r'^perfil/$','perfil_view',name='vista_perfil'),
	url(r'^nuevaclave/$','nuevaclave_view',name='vista_nuevaclave'),
	url(r'^bandejaentrada/$','bandejaentrada_view',name='vista_bandejaentrada'),
	url(r'^editarperfil/$','editarperfil_view',name='vista_editarperfil'),
	url(r'^detalle/socio/(\d+)/$','detalle_socio_view',name='vista_detalle_socio'),
	url(r'^detalle/socio/$','detalle_socio_folio_view',name='vista_detalle_socio_folio'),
	url(r'^enviarPM/$','enviar_mensaje_view',name='enviar_mensaje_personal'),
	url(r'^busqueda/avanzada/$','busqueda_view',name='busqueda_avanzada'),
	url(r'^resultados/$','resultados_view',name='vista_resultados'),
	url(r'^todosresultados/$','resultados_completos',name='vista_resultados_completos'),
	url(r'^mensaje/(\d+)/$','mensaje_view',name='vista_mensaje'),
	url(r'^eliminar/mensaje/(\d+)/$','eliminarmensaje_view',name='vista_eliminarmensaje'),
	url(r'^pago/perfil/$','pagoperfil_view',name='vista_pagoperfil'),
	url(r'^listadopagos/$','listado_view',name='vista_listado'),
	url(r'^infopago/$','infopago_view',name='vista_infopago'),
)    

