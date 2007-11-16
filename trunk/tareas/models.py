from django.db import models
from django.contrib.auth.models import User
from abuelas.seguimiento.models import Causa

class Prioridad(models.Model):
    nombre_prioridad = models.CharField("Nombre", maxlength=40, unique=True)
    orden = models.IntegerField()
    color = models.CharField(maxlength=40, null=True, blank=True)

    def __str__(self):
        return self.nombre_prioridad

    class Meta:
        ordering = ['orden']

    class Admin:
        pass


class Tarea(models.Model):
    descripcion = models.CharField(maxlength=255)
    asignado = models.ForeignKey(User)
    priority = models.ForeignKey(Prioridad)    
    vencimiento = models.DateTimeField(null=True, blank=True)
    causa = models.ForeignKey(Causa, null=True, blank=True, verbose_name="Relacionada a la causa")
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    completado = models.DateTimeField(null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.descripcion

    class Admin:
        pass


