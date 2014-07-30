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
	('anu','Anulado'),
)
tipoContrato=(
	('inde','Indefinido'),
	('def','Definido'),
	('otr','Otro'),
)
planes=(
	('1','Plan 1: $6000 - 6 meses'),
	('2','Plan 2: $8000 - 8 meses'),
	('3','Plan 3: $11000 - 12 meses'),
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
hijos=(
	('s','Si'),
	('n','No'),
)
renta=(
	('0','< 200.000'),
	('1','200.000-450.000'),
	('2','450.000-650.000'),
	('3','650.000-850.000'),
	('4','850.000-1.000.000'),
	('5','1.250.000-1.500.000'),
	('6','1.500.000-1.750.000'),
	('7','2.000.000-2.500.000'),
	('8','2.500.000-3.000.000'),
	('9','3.000.000 o +'),
)
estados=(
	('0', 'Activo'),
	('1', 'Inactivo'),
	)
disp=(
	('0', 'Inmediata'),
	('1', '30 días'),
	('2', '60 días'),
	('3', '90 días'),
	)

class Nacionalidad(models.Model):
	id 				  = models.AutoField('ID', primary_key=True)
	nombre 			  = models.CharField('Nombre', max_length=64, null=False, blank=False)

	def __unicode__(self):
		return u'%s' % (self.nombre)

class Socio(models.Model):
	id                = models.AutoField('ID', primary_key=True)
	nombre            = models.CharField('Nombre', max_length=64,null=True, blank=True)
	telefono          = models.IntegerField("Teléfono", null=True, blank=True)
	web               = models.CharField('Web' ,max_length=128, null=True, blank=True)
	edad              = models.IntegerField('Edad', null=True, blank=True)
	sexo              = models.CharField("Sexo",max_length=10, choices=sexo, null=True, blank=True)
	tiene_hijos       = models.CharField('¿Tiene hijos?',max_length=10, choices=hijos, null=True, blank=True)
	estado_civil      = models.CharField('Estado Civil',max_length=10, choices=estadoCivil, null=True, blank=True)
	pretencion_renta  = models.CharField("Pretenciones de Renta", max_length=10, choices=renta, null=True, blank=True)
	tipo_contrato     = models.CharField('Tipo de Contrato',max_length=10, choices=tipoContrato, null=True, blank=True)
	comentario_est	  = models.CharField('Comentario' ,max_length=512, null=True, blank=True)
	folio			  = models.CharField('Folio', max_length=10, null=False, blank=False, unique=True)
	magister		  = models.BooleanField('Magister')
	doctorado 		  = models.BooleanField('Doctorado')
	disponibilidad    = models.CharField('Disponibilidad', max_length=10, choices=disp, null=True, blank=True)
	disponibilidadV	  = models.BooleanField('Dispopnibilidad de vehiculo')
	cargo_extra 	  = models.CharField('Cargos extra' ,max_length=512, null=True, blank=True)
	activo 			  = models.CharField('Estado', max_length=2, choices=estados, default="1")
	
	nacionalidad  =models.ForeignKey(Nacionalidad, verbose_name="Nacionalidad", null=True, blank=True)
	user = models.OneToOneField(User)
	

class RegistroPago(models.Model):
	id           = models.AutoField('ID', primary_key=True)
	fecha_inicio = models.DateTimeField('Fecha Inicio',editable=False, auto_now=True)
	fecha_fin    = models.DateTimeField('Fecha Fin',editable=False)
	plan         = models.CharField('Plan', max_length=7,choices=planes, default="1")

	# Llaves foraneas
	socio        = models.ForeignKey(Socio, verbose_name="Socio")

	def __unicode__(self):
		return u'%s %s' % (self.socio.usuario, self.fecha_inicio)
	class Meta:
		ordering = ["fecha_inicio"]

	def __unicode__(self):
		return u'%s [%s-%s]' % (self.socio, self.fecha_inicio, self.fecha_fin)


class Mensaje(models.Model):
	id              = models.AutoField('ID', primary_key=True)
	fecha           = models.DateTimeField('Fecha',editable=False)
	contenido       = models.CharField('Mensaje', max_length=440,null=False, blank=False)
	nombre_contacto = models.CharField('Nombre', max_length=25,null=False, blank=False)
	medio_contacto  = models.CharField('Contacto', max_length=25,null=False, blank=False)
	leido 			= models.BooleanField('Leido',default=False) 

	# Llaves foraneas
	socio           = models.ForeignKey(Socio, verbose_name="Socio")
	def __unicode__(self):
		return u'(%s) %s' % (self.fecha, self.socio)

class TipoHabilidad(models.Model):
	id     = models.AutoField('ID', primary_key=True)
	nombre = models.CharField('Nombre', max_length=128,null=False, blank=False)

	def __unicode__(self):
		return u'%s' % (self.nombre)


class Habilidad(models.Model):
	id            = models.AutoField('ID', primary_key=True)
	nombre        = models.CharField('Nombre', max_length=128,null=False, blank=False)

	# Llaves foraneas
	tipoHabilidad = models.ForeignKey(TipoHabilidad, verbose_name="Tipo")

	def __unicode__(self):
		return u'%s' % (self.nombre)
	class Meta:
		ordering = ["nombre"]

class OtrasHabilidades(models.Model):
	id        = models.AutoField('ID', primary_key=True)
	nivel     = models.CharField('Nivel', max_length=7,choices=nivelHabilidad, null=True, blank=True)

	# Llaves foraneas
	socio     = models.ForeignKey(Socio, verbose_name="Socio")
	habilidad = models.ForeignKey(Habilidad, verbose_name="Habilidad", null=True, blank=True)



class Rubro(models.Model):
	id     = models.AutoField('ID', primary_key=True)
	nombre = models.CharField('Nombre', max_length=128,null=False, blank=False)

	def __unicode__(self):
		return u'%s' % (self.nombre)
	class Meta:
		ordering = ["nombre"]	

class Cargo(models.Model):
	id     = models.AutoField('ID', primary_key=True)
	nombre = models.CharField('Nombre', max_length=250,null=False, blank=False)

	def __unicode__(self):
		return u'%s' % (self.nombre)
	class Meta:	
		ordering = ["nombre"]

class EmpleoBuscado(models.Model):
	id    = models.AutoField('ID', primary_key=True)

	# Llaves foraneas
	socio = models.ForeignKey(Socio, verbose_name="Socio")
	cargo = models.ForeignKey(Cargo, verbose_name="Cargo", null=True, blank=True)



class ExperienciaLaboral(models.Model):
	id              = models.AutoField('ID', primary_key=True)
	desde           = models.IntegerField("Desde", null=True, blank=True)
	hasta           = models.IntegerField("Hasta", null=True, blank=True)
	comentario      = models.CharField('Comentario', max_length=512, blank=True)

	# Llaves foraneas
	cargo       = models.ForeignKey(Cargo, verbose_name="Cargo", null=True, blank=True)
	socio       = models.ForeignKey(Socio, verbose_name="Socio")
	rubro       = models.ForeignKey(Rubro, verbose_name="Rubro", null=True, blank=True)


class Titulo(models.Model):
	id      = models.AutoField('ID', primary_key=True)
	nombre  = models.CharField('Nombre', max_length=128,null=False, blank=False)
	tipo    = models.CharField('Tipo', max_length=7, choices=tipoTitulo, default="t")

	def __unicode__(self):
		return u'%s' % (self.nombre)
	class Meta:
		ordering = ["nombre"]

class Institucion(models.Model):
	id      = models.AutoField('ID', primary_key=True)
	nombre  = models.CharField('Nombre', max_length=128,null=False, blank=False)
	colegio = models.BooleanField('Colegio') 

	def __unicode__(self):
		return u'%s' % (self.nombre)
	class Meta:
		ordering = ["nombre"]

class Estudios(models.Model):
	id          = models.AutoField('ID', primary_key=True)
	estado      = models.CharField('Estado', max_length=7, choices=estadoEstudio, null=True, blank=True)

	# Llaves foraneas
	titulo      = models.ForeignKey(Titulo, verbose_name="Titulo", null=True, blank=True)
	institucion = models.ForeignKey(Institucion, verbose_name="Institucion", null=True, blank=True)
	socio       = models.ForeignKey(Socio, verbose_name="Socio")


#Ver bien el funcuionamiento de esta tabla
class TitulosEnInstituciones(models.Model):
	#tabla resultante de una relacion n-n
	id          = models.AutoField('ID', primary_key=True)

	#llaves foraneas
	titulo      = models.ForeignKey(Titulo, verbose_name="Titulo")
	institucion = models.ForeignKey(Institucion, verbose_name="Institucion")


class Localidad(models.Model):
	id     = models.AutoField('ID', primary_key=True)
	nombre = models.CharField('Nombre', max_length=128,null=False, blank=False)
	tipo   = models.CharField('Tipo', max_length=7, choices=tipoLocalidad, default="c")

	localidadPadre = models.ForeignKey('self', null=True, blank=True,verbose_name="Pertenece a")
	
	def __unicode__(self):
		return u'%s' % (self.nombre)
	class Meta:
		ordering = ["nombre"]

class LocalidadConSocio(models.Model):
#tabla resultante de una relacion n-n
	id        = models.AutoField('ID', primary_key=True)

	#llaves foraneas
	socio     = models.ForeignKey(Socio, verbose_name="Socio")
	localidad = models.ForeignKey(Localidad, verbose_name="Localidad", null=True, blank=True)



