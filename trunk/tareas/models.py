# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from abuelas.seguimiento.models import Caso

class Proyecto(models.Model):
    nombre = models.CharField(u'Nombre del proyecto', maxlength=255)
    fechaInicio =  models.DateField(u'Fecha de inicio', auto_now=True)
    caso = models.ForeignKey(Caso, null=True, blank=True, verbose_name="Proyecto relacionado al caso", help_text=u'Dejá el campo en blanco si se trata de otro tipo de proyecto.' )    
    fechaCierre = models.DateField(u'Fecha de finalización', null=True, blank=True, help_text=u'Dejá este campo en blanco si el proyecto no está finalizado')
    descripcion = models.TextField(blank=True)

    def __unicode__(self):
        return self.nombre
        
    class Admin:
        pass
    


class Tarea(models.Model):
    OPCIONES = ((1,u'Urgente'), (2,u'Importante'), (3,u'Normal'), (4,u'Tranqui'), (5,u'Cuando sea'))
    descripcion = models.CharField(maxlength=255)
    asignado = models.ManyToManyField(User,verbose_name="Tarea asignada a", null=True, blank=True, help_text="Dejar en blanco para que cualquiera pueda ver las tareas del staff")
    fechaCreacion = models.DateTimeField(auto_now_add=True)    
    prioridad = models.SmallIntegerField(choices=OPCIONES)
    proyecto = models.ForeignKey(Proyecto)
    vencimiento = models.DateTimeField(null=True, blank=True, help_text="Si esta tarea tiene un vencimiento, indique la fecha y la hora")
    completado = models.DateTimeField(null=True, blank=True, help_text=u'Dejá este campo en blanco si la tarea no está finalizada')
    comentario = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.descripcion + "(Prioridad: " + OPCIONES[prioridad-1][1] + ")"

    class Admin:
		list_filter = ('prioridad', 'vencimiento', 'asignado', 'completado')
		search_fields = ['@descripcion', '@comentario']
		list_display = ('fechaCreacion','prioridad', 'proyecto', 'descripcion', 'completado')

