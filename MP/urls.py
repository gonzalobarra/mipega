from django.conf.urls import patterns,url

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
)    

