#!/usr/bin/env python
#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from abuelas.casos.models import Caso, Testigo
from abuelas.documentos.models import Documento
from abuelas.incidentes.models import Incidente
from abuelas.tareas.models import Tarea


class CategoriaSeguimiento(models.Model):
    nombre = models.CharField(u'Nombre', max_length=100, unique=True, help_text=u'Ej: Declaración, Presentación de Prueba, etc' )

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = u'Categorías de seguimiento'

    class Admin:
        pass


class Seguimiento(models.Model):
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User)	
    categoria = models.ForeignKey(CategoriaSeguimiento, name=u'Categoría')
    causa = models.ForeignKey(Caso, name="Caso")
    foja = models.CharField(max_length=20) 
    importante = models.BooleanField()
    vencimiento = models.ForeignKey(Tarea, name="Vencimiento", null=True, blank=True, help_text=u'Asociar tarea a este seguimiento')
    comentario = models.TextField()

    def __unicode__(self):
        return "seguimiento " + str(self.fecha_ingreso)

    class Admin:
        list_display = ('fecha_ingreso','creado_por', 'causa', 'foja', 'comentario', 'vencimiento')
        list_display_links = ('fecha_ingreso', 'causa')
        list_filter = ('causa','fecha_ingreso','categoria', 'creado_por')        
        ordering = ['fecha_ingreso','causa']

    class Meta:
        order_with_respect_to = 'causa'

class SeguimientoIncidente(models.Model):
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User)
    #incidente = models.ForeignKey(Incidente)
    foja = models.CharField(max_length=20)
    comentario = models.TextField()

    def __unicode__(self):
        return "seguimiento Incidente" + str(self.fecha_ingreso)

    class Admin:
        date_hierarchy = 'fecha_ingreso'
        fields = ((None, {'fields': (('fecha_ingreso', 'foja'),
            ('incidente','creado_por'), 'comentario',)}),
            ('Opciones avanzadas', {'classes': 'collapse','fields': 
            ('vencimiento', )}),)