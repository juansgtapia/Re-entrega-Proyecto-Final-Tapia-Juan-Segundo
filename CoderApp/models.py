from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Catedra(models.Model):
    nombre_de_la_materia = models.CharField(max_length=40, unique=True)
    año = models.IntegerField()

    def __str__(self):
        return f"Curso: {self.nombre_de_la_materia}, año: {self.año}"

class Estudiante(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    calificacion = models.IntegerField()

    def __str__(self):
        return f"Nombre del estudiante: {self.nombre} {self.apellido} \nEmail: {self.email} \nCalificación: {self.calificacion}"

class Profesor(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Nombre del profesor: {self.nombre} {self.apellido} \nEmail: {self.email}"

class Entregado(models.Model):
    trabajo_entregado = models.BooleanField()

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avatares", null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.imagen}"

class Post(models.Model):
    titulo = models.CharField(max_length=99, unique=True, null=True)
    imagen_post = models.ImageField(upload_to="imagenesposteadas", null=True, blank=True)
    descripcion = models.CharField(max_length=99, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} -- {self.titulo} -- {self.descripcion} -- {self.imagen_post}"

