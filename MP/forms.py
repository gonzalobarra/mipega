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
    ClaveRepetida = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}),required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}),required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)
    class Meta:
        model = User
        fields = ('username', 'password','email',)
    

class SocioForm(forms.ModelForm):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)    
    telefono = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)
    web = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)
    ano_nacimiento = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)
    tiene_hijos = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class' : 'form-control'}),required=False)
    sexo = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}), required=False)
    estado_civil = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}),required=False)
    pretencion_renta = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)
    tipo_contrato = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}),required=False)

    class Meta:
        model = Socio
        fields = ('usuario','telefono', 'web', 'ano_nacimiento', 'sexo','tiene_hijos', 'estado_civil', 'pretencion_renta', 'tipo_contrato',)

class LocalidadconSocioForm(forms.ModelForm):
    localidad = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}), required=False)
    class Meta:
        model = LocalidadConSocio
        fields = ('localidad',)

class EstudioForm(forms.ModelForm):
    ano = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)
    estado = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}), required=False)
    titulo = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}), required=False)
    institucion = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}), required=False)
    class Meta:
        model = Estudios
        fields = ('ano', 'estado', 'titulo', 'institucion')

class ExperienciaLaboralForm(forms.ModelForm):
    ano_ingreso = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)
    ano_egreso = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False)
    cargo = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}), required=False)
    rubro = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}), required=False)

    class Meta:
        model = ExperienciaLaboral
        fields = ('ano_ingreso', 'ano_egreso', 'cargo', 'rubro',)

class OtrasHabilidadesForm(forms.ModelForm):
    nivel = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}), required=False)
    habilidad = forms.CharField(widget=forms.Select(attrs={'class' : 'form-control'}), required=False)

    class Meta:
        model = OtrasHabilidades
        fields = ('nivel', 'habilidad',)                        
