from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import datetime
from django import forms
from django.core.validators import RegexValidator


# Create your models here.


#MODELO PARA CRUD DE 


class Vehiculo(models.Model):
    solo_numeros = RegexValidator(r'^\d{1,10}$', message="Solo se permiten hasta 10 números y sin caracteres especiales.")
    placa = models.CharField(max_length=6, primary_key=True, blank=False)
    marca = models.CharField(max_length=20, blank=False)
    
    def year_choices():
        return [(r, r) for r in range(1900, datetime.date.today().year + 1)]

    def current_year():
        return datetime.date.today().year

    modelo = models.PositiveSmallIntegerField(
        choices=year_choices(),
        default=current_year(),
        verbose_name="Año"
    )
    
    color = models.CharField(max_length=30, blank=False)
    propietario = models.CharField(max_length=100,blank=False)
    ID = models.IntegerField( null=True, blank=False)
    telefono = models.CharField( max_length=10,validators=[solo_numeros] ,null=True, blank=False)
    Correo= models.EmailField(max_length=254,  null=True, blank=False)
    diagnostico = models.TextField( null=True, blank=False)
    fecha_ingreso = models.DateField( null=True, blank=False)
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=False)
    
    
    

    def __str__(self):
        return f"{self.placa} - {self.marca}"
    
    
    
#Modelo de guardar vehiculo eliminado

class VehiculoEliminado(models.Model):
    placa = models.CharField(max_length=20)
    motivo = models.TextField()
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.placa} - {self.fecha}"


    
#MODELO PARA CRUD DE TAREAS

class Tarea(models.Model):

    ESTADOS = (
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Finalizada', 'Finalizada'),
    )

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    
    tecnico = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)

    descripcion = models.CharField(max_length=255)

    fecha_creacion = models.DateField(auto_now_add=True)

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Pendiente'
    )
    
    


    def __str__(self):
        return f"{self.vehiculo.placa} - {self.estado} - {self.descripcion}"
    
    
#Tareas eliminadas

class TareaEliminada(models.Model):

    vehiculo = models.CharField(max_length=20)

    descripcion = models.CharField(max_length=255)

    estado = models.CharField(max_length=20)

    motivo = models.TextField()

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - {self.fecha}"