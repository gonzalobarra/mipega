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

class LocalidadconSocioForm(forms.ModelForm):
    class Meta:
        model = LocalidadConSocio
        fields = ('localidad',)

class EstudioForm(forms.ModelForm):
    class Meta:
        model = Estudios

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral

class OtrasHabilidadesForm(forms.ModelForm):
    class Meta:
        model = OtrasHabilidades                        