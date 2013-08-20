#!/usr/bin/python
# -*- coding: Utf8 -*-
from django import forms
from django.forms.widgets import Input
from datetime import date
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect
from MP.models import *
from django.contrib.auth.models import User
from django.contrib.localflavor.cl.forms import CLRutField, CLRegionSelect

class Html5DateInput(Input):
    input_type = 'date'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)
    #ClaveRepetida = forms.CharField(widget=forms.PasswordInput,required=False,label='Repita su clave')

class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ('usuario','email','telefono', 'web', 'ano_nacimiento', 'sexo','tiene_hijos', 'estado_civil', 'pretencion_renta', 'tipo_contrato',)

class LocalidadconSocioForm(forms.ModelForm):
    class Meta:
        model = LocalidadConSocio
        fields = ('localidad',)

class EstudioForm(forms.ModelForm):
    class Meta:
        model = Estudios
        fields = ('ano', 'estado', 'titulo', 'institucion')

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = ('ano_ingreso', 'ano_egreso', 'cargo', 'rubro',)

class OtrasHabilidadesForm(forms.ModelForm):
    class Meta:
        model = OtrasHabilidades
        fields = ('nivel', 'habilidad',)                        