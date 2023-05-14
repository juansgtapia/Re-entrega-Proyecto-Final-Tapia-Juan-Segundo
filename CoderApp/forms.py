from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from CoderApp.models import Post

class catedraform(forms.Form):
    nombre_de_la_materia = forms.CharField(max_length=40)
    año = forms.IntegerField()

class estudiantesform(forms.Form):
    nombre = forms.CharField(max_length=40)
    apellido = forms.CharField(max_length=40)
    email = forms.EmailField()
    calificacion = forms.IntegerField()

class profesoresform(forms.Form):
    nombre = forms.CharField(max_length=40)
    apellido = forms.CharField(max_length=40)
    email = forms.EmailField()

class entregadoforms(forms.Form):
    trabajo_entregado = forms.BooleanField()

class buscarcurso(forms.Form):
    nombre_de_la_materia = forms.CharField()

class buscarestudiante(forms.Form):
    nombre_del_estudiante = forms.CharField()

class UserEditForm(UserCreationForm):

    email = forms.EmailField(label="Modificar tu email")
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir la contraseña', widget=forms.PasswordInput) 

    class Meta:
        model = User
        fields = [ 'email', 'password1', 'password2'] 
        help_texts = {k:"" for k in fields}

class AvatarFormulario(forms.Form):
    imagen = forms.ImageField(required=True)

from PIL import Image

class PosteoFormulario(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'descripcion', 'imagen_post')
        labels = {
            'titulo': 'Escribe un título',
            'descripcion': 'Escribe una descripción',
        }


