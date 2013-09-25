# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import authenticate, login
from datetime import date,timedelta
from calendar import mdays

sexo=(
	('m','Masculino'),
	('f','Femenino'),
)
estadoCivil=(
	('sol','Soltero'),
	('cas','Casado'),
	('div','Divorciado'),
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
nivelHabilidad=(
	('u','Usuario'),
	('m','Medio'),
	('a','Avanzado'),
)
estadoEstudio=(
	('i','Incompleto'),
	('c','Cursando'),
	('co','Completo'),
)
tipoTitulo=(
	('t','Tecnico'),
	('tp','Tecnico Profesional'),
	('p','Profesional'),
)
tipoLocalidad=(
	('c','Comuna'),
	('r','Región'),
)
nacionalidad=(
	('cl', 'Chile'),
)
nacimiento=(
	('0','18-25'),
	('1','26-35'),
	('2','36-45'),
	('3','46-55'),
	('4','56+'),
)
hijos=(
	('s','Si'),
	('n','No'),
)
renta=(
	('0','100-500'),
	('1','500-700'),
)

class Socio(models.Model):
	id                = models.AutoField('ID', primary_key=True)
	usuario           = models.CharField('Nombre', max_length=64,null=False, blank=False)
	telefono          = models.IntegerField("Teléfono", null=True, blank=True)
	web               = models.CharField('Email' ,max_length=64, null=True, blank=True)
	ano_nacimiento    = models.CharField('Año de nacimiento',max_length=10, choices=nacimiento)
	sexo              = models.CharField("Sexo",max_length=10, choices=sexo)
	tiene_hijos       = models.CharField('¿Tiene hijos?',max_length=10, choices=hijos)
	estado_civil      = models.CharField('Estado Civil',max_length=10, choices=estadoCivil)
	pretencion_renta  = models.CharField("Pretenciones de Renta", max_length=10, choices=renta)
	tipo_contrato     = models.CharField('Tipo de Contrato',max_length=10, choices=tipoContrato)
	nacionalidad	  = models.CharField('Nacionalidad',max_length=10, choices=nacionalidad)
	comentario        = models.CharField('Comentario' ,max_length=512, null=True, blank=True)
	comentario_est	  = models.CharField('Comentario' ,max_length=512, null=True, blank=True)
	
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

class TipoHabilidad(models.Model):
	id     = models.AutoField('ID', primary_key=True)
	nombre = models.CharField('Nombre', max_length=32,null=False, blank=False)


class Habilidad(models.Model):
	id            = models.AutoField('ID', primary_key=True)
	nombre        = models.CharField('Nombre', max_length=32,null=False, blank=False)

	# Llaves foraneas
	tipoHabilidad = models.ForeignKey(TipoHabilidad, verbose_name="Tipo")

	def __unicode__(self):
		return u'%s' % (self.nombre)	

class OtrasHabilidades(models.Model):
	id        = models.AutoField('ID', primary_key=True)
	nivel     = models.CharField('Nivel', max_length=7,choices=nivelHabilidad, default="u")

	# Llaves foraneas
	socio     = models.ForeignKey(Socio, verbose_name="Socio")
	habilidad = models.ForeignKey(Habilidad, verbose_name="Habilidad")


class Rubro(models.Model):
	id     = models.AutoField('ID', primary_key=True)
	nombre = models.CharField('Nombre', max_length=32,null=False, blank=False)

	def __unicode__(self):
		return u'%s' % (self.nombre)

class Cargo(models.Model):
	id     = models.AutoField('ID', primary_key=True)
	nombre = models.CharField('Nombre', max_length=32,null=False, blank=False)

	def __unicode__(self):
		return u'%s' % (self.nombre)

class EmpleoBuscado(models.Model):
	id    = models.AutoField('ID', primary_key=True)

	# Llaves foraneas
	socio = models.ForeignKey(Socio, verbose_name="Socio")
	cargo = models.ForeignKey(Cargo, verbose_name="Cargo")



class ExperienciaLaboral(models.Model):
	id          = models.AutoField('ID', primary_key=True)
	ano_ingreso = models.IntegerField("Año Ingreso", null=False, blank=False)
	ano_egreso  = models.IntegerField("Año Egreso", null=True, blank=True)

	# Llaves foraneas
	cargo       = models.ForeignKey(Cargo, verbose_name="Cargo")
	socio       = models.ForeignKey(Socio, verbose_name="Socio")
	rubro       = models.ForeignKey(Rubro, verbose_name="Rubro")


class Titulo(models.Model):
	id      = models.AutoField('ID', primary_key=True)
	nombre  = models.CharField('Nombre', max_length=32,null=False, blank=False)
	tipo    = models.CharField('Tipo', max_length=7, choices=tipoTitulo, default="t")
	colegio = models.BooleanField('Colegio')

	def __unicode__(self):
		return u'%s' % (self.nombre)

class Institucion(models.Model):
	id      = models.AutoField('ID', primary_key=True)
	nombre  = models.CharField('Nombre', max_length=32,null=False, blank=False)
	tipo    = models.CharField('Tipo', max_length=7, choices=tipoTitulo, default="t")
	colegio = models.BooleanField('Colegio') 

	def __unicode__(self):
		return u'%s' % (self.nombre)

class Estudios(models.Model):
	id          = models.AutoField('ID', primary_key=True)
	estado      = models.CharField('Estado', max_length=7, choices=estadoEstudio, default="i")

	# Llaves foraneas
	titulo      = models.ForeignKey(Titulo, verbose_name="Titulo")
	institucion = models.ForeignKey(Institucion, verbose_name="Institucion")
	socio       = models.ForeignKey(Socio, verbose_name="Socio")



class TitulosEnInstituciones(models.Model):
	#tabla resultante de una relacion n-n
	id          = models.AutoField('ID', primary_key=True)

	#llaves foraneas
	titulo      = models.ForeignKey(Titulo, verbose_name="Titulo")
	institucion = models.ForeignKey(Institucion, verbose_name="Institucion")


class Localidad(models.Model):
	id     = models.AutoField('ID', primary_key=True)
	nombre = models.CharField('Nombre', max_length=32,null=False, blank=False)
	tipo   = models.CharField('Tipo', max_length=7, choices=tipoLocalidad, default="c")

	#localidadPadre = models.ForeignKey(Localidad, verbose_name="Localidad Padre")
	def __unicode__(self):
		return u'%s' % (self.nombre)

class LocalidadConSocio(models.Model):
#tabla resultante de una relacion n-n
	id        = models.AutoField('ID', primary_key=True)

	#llaves foraneas
	socio     = models.ForeignKey(Socio, verbose_name="Socio")
	localidad = models.ForeignKey(Localidad, verbose_name="Localidad")



