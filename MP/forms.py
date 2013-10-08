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


RANGO = (
    ('1','18-22'),
    ('2','23-29'),
    ('3','29-37'),
    ('4','38-44'),
    ('5','44+'),
    )

SEXO = (
    ('m','Masculino'),
    ('f','Femenino'),
    )


class Html5DateInput(Input):
    input_type = 'date'

class UserForm(forms.ModelForm):
    ClaveRepetida = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True,label='Repita su clave')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True,label='Clave')
    class Meta:
        model = User
        fields = ('username', 'password','email',)
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),  
            'password': forms.PasswordInput(attrs={'class':'form-control'}), 
            'email': forms.TextInput(attrs={'class':'form-control plain-field'}),       
        }
    
class SocioForm(forms.ModelForm):
    comentario_est = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta:
        model = Socio
        fields = ('nombre','telefono', 'web', 'ano_nacimiento', 'comentario_est','nacionalidad','magister','doctorado','sexo','tiene_hijos', 'estado_civil', 'pretencion_renta', 'tipo_contrato', 'nacionalidad',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control plain-field'}),
            'web': forms.TextInput(attrs={'class':'form-control plain-field'}),
            'ano_nacimiento': forms.Select(attrs={'class':'form-control'}),
            'sexo': forms.Select(attrs={'class':'form-control'}),
            'estado_civil': forms.Select(attrs={'class':'form-control'}),
            'pretencion_renta': forms.Select(attrs={'class':'form-control'}),
            'tipo_contrato': forms.Select(attrs={'class':'form-control'}),
            'tiene_hijos': forms.Select(attrs={'class':'form-control'}),
            'nacionalidad': forms.Select(attrs={'class':'form-control'}),
        }

class LocalidadconSocioForm(forms.Form):
    localidad = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,label='localidad')

class EstudioForm(forms.ModelForm):
    class Meta:
        model = Estudios
        fields = ('estado', 'titulo', 'institucion')
        widgets = {
            'estado': forms.Select(attrs={'class':'form-control'}),
            'titulo': forms.Select(attrs={'class':'form-control'}),
            'institucion': forms.Select(attrs={'class':'form-control'}),        
        }

class ExperienciaLaboralForm(forms.ModelForm):
    comentario = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta:
        model = ExperienciaLaboral
        fields = ('anos_trabajados', 'cargo', 'rubro','comentario')
        widgets = {
            'anos_trabajados': forms.TextInput(attrs={'class':'form-control'}),
            'cargo': forms.Select(attrs={'class':'form-control'}),
            'rubro': forms.Select(attrs={'class':'form-control'}),        
        }

class OtrasHabilidadesForm(forms.ModelForm):
    class Meta:
        model = OtrasHabilidades
        fields = ('nivel', 'habilidad',) 
        widgets = {
            'nivel': forms.Select(attrs={'class':'form-control'}),
            'habilidad': forms.Select(attrs={'class':'form-control'}),        
        }
                       
class BuscaRapidaForm(forms.Form):

    cargo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,label='Cargo')
    rango_etario = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),required=False,label='Rango etario', choices=RANGO)
    localidad = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,label='Localidad')
    sexo = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control'}),choices=SEXO)


class LoginForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class cambiarClave(forms.Form):
    ClaveAntigua = forms.CharField(max_length=20,  widget= forms.PasswordInput(attrs={'class':'form-control'}),label='Clave antigua')
    ClaveNueva = forms.CharField(max_length=20,  widget= forms.PasswordInput(attrs={'class':'form-control'}),label='Clave nueva:')
    ClaveRepetida = forms.CharField(max_length=20, widget= forms.PasswordInput(attrs={'class':'form-control'}),label='Clave nueva (confirmación):')   

class EmpleoBuscadoForm(forms.Form):
    cargo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,label='Cargo')
    
