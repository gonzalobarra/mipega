from django.db import models

# -*- coding: Utf8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import authenticate, login
from datetime import date,timedelta
from calendar import mdays
from django.contrib.localflavor.cl.forms import CLRutField

sexo=(
	('i','Indiferente'),
	('m','Masculino'),
	('f','Femenino'),
)
estadoCivil=(
	('sol','Soltero'),
	('cas','Casado'),
	('sep','Separado'),
	('viu','Viudo'),
)
tipoContrato=(
	('indi','Me es Indferente'),
	('inde','Indefinido'),
	('def','Definido'),
	('otr','Otro'),
)
planes=(
	('1','Plan 1'),
	('2','Plan 2'),
	('3','Plan 3'),
)

class RutField(models.CharField):
	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = kwargs.get('max_length', 12)
		models.CharField.__init__(self, *args, **kwargs)
		
	def formfield(self, **kwargs):
		defaults = {'form_class': CLRutField}
		defaults.update(kwargs)
		return super(RutField, self).formfield(**defaults)

class Socio(models.Model):
	id                = models.AutoField('ID', primary_key=True)
	usuario           = RutField('RUT',unique= True,help_text='ejemplo: 12.345.678-K')
	email             = models.CharField('Email' ,max_length=64, null=True, blank=True)
	telefono          = models.IntegerField("Teléfono", null=True, blank=True)
	web               = models.CharField('Email' ,max_length=64, null=True, blank=True)
	año_nacimiento    = models.IntegerField("Año Nacimiento", null=True, blank=True)
	sexo              = models.CharField("Sexo",max_length=7, choices=sexo, default='Ind')
	tiene_hijos       = models.BooleanField('Tiene Hijos?')
	estado_civil      = models.CharField('Estado Civil',max_length=7, choices=estadoCivil, default='Sol')
	pretencion_renta  = models.IntegerField("Pretenciones de Renta", null=True, blank=True)
	tipo_contrato     = models.CharField('Tipo de Contrato',max_length=7, choices=tipoContrato, default='Ind')
	
	user = models.OneToOneField(User)

	def __unicode__(self):
		return u'%s' % (self.usuario)

class RegistroPago(models.Model):
	id           = models.AutoField('ID', primary_key=True)
	fecha_inicio = models.DateTimeField('Fecha Inicio',editable=False)
	fecha_fin    = models.DateTimeField('Fecha Fin',editable=False)
	monto        = models.IntegerField("Monto de Pago", null=False)
	plan         = models.CharField('Plan', max_length=7,choices=planes, default="1")

	# Llaves foraneas
	socio        = models.ForeignKey(Socio, verbose_name="Socio")

	def __unicode__(self):
		return u'%s %s' % (self.socio.usuario, self.fecha_inicio)


class Mensaje(models.Model):
	id              = models.AutoField('ID', primary_key=True)
	fecha           = models.DateTimeField('Fecha',editable=False)
	contenido       = models.CharField('Mensaje', max_length=440,null=False, blank=False)
	nombre_contacto = models.CharField('Nombre', max_length=25,null=False, blank=False)
	medio_contacto  = models.CharField('Contacto', max_length=25,null=False, blank=False)

	# Llaves foraneas
	socio           = models.ForeignKey(Socio, verbose_name="Socio")

class OtrasHabilidades(models.Model):
	id = models.AutoField('ID', primary_key=True)
	nivel = 

	# Llaves foraneas
	socio = models.ForeignKey(Socio, verbose_name="Socio")
	habilidad = models.ForeignKey(Habilidad, verbose_name="Habilidad")

class Habilidad(model.Models):
	id = models.AutoField('ID', primary_key=True)
	nombre = 

	# Llaves foraneas
	tipoHabilidad = models.ForeignKey(TipoHabilidad, verbose_name="Tipo")

class TipoHabilidad(model.Models):
	id              = models.AutoField('ID', primary_key=True)
	nombre = 


class Rubro(model.Models):
	id = models.AutoField('ID', primary_key=True)
	nombre = 

class EmpleoBuscado(model.Models):
	id              = models.AutoField('ID', primary_key=True)

	# Llaves foraneas
	socio
	cargo



class ExperienciaLaboral(model.Models):
	id              = models.AutoField('ID', primary_key=True)
	año_ingreso
	año_egreso
	# Llaves foraneas
	cargo
	socio
	rubro



class Estudios(model.Models):
	id              = models.AutoField('ID', primary_key=True)
	año
	estado

	# Llaves foraneas
	titulo
	institucion


class Titulos(model.Models):
	id              = models.AutoField('ID', primary_key=True)
	nombre
	tipo #tecnica, tecnico profesional, profesional
	



class Institucion(model.Models):
	id              = models.AutoField('ID', primary_key=True)
	nombre
	tipo





class TitulosEnInstituciones(model.Models):
	#tabla resultante de una relacion n-n
	id              = models.AutoField('ID', primary_key=True)

	#llaves foraneas
	titulo
	institucion


class Cargo(model.Models):
	id              = models.AutoField('ID', primary_key=True)
	nombre


class LocalidadConSocio(model.Models):
#tabla resultante de una relacion n-n
	id              = models.AutoField('ID', primary_key=True)

	#llaves foraneas
	socio
	localidad


