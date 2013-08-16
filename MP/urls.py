from django.conf.urls import patterns,url

urlpatterns = patterns('MP.views',
	url(r'^$','index_view',name='vista_principal'),
	url(r'^registro/$','registro_view',name='vista_registro'),
)    

