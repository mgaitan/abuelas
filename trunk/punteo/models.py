#!/usr/bin/env python
#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from abuelas.casos.models import Documento, Caso, Testigo, Imputado



class ParrafoPunteo(models.Model):
    """Punteo"""
    caso = models.ForeignKey(Caso)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User)
    texto = models.TextField()
    adjuntos = models.ManyToManyField(Documento, null=True, blank=True)

    def __unicode__(self):
        return self.texto
        
    


class CategoriaMarcasPunteo(models.Model):
    nombre = models.CharField(u'Categoría de marcas de punteo', max_length=100, unique=True)
    
    def __unicode__(self):
         return self.nombre
    
    class Meta:
        verbose_name_plural = u'Categorías de marcas de punteo'
        
class MarcasPunteo(models.Model):
    parrafo = models.ForeignKey(ParrafoPunteo)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User)
    categoria = models.ForeignKey(CategoriaMarcasPunteo)
    fecha_incidente = models.DateField(u'Fecha relacionada', blank=True, null=True)
    comentario = models.TextField(u'Comentario')
    imputados = models.ManyToManyField(Imputado, verbose_name=u'Imputados relacionados', blank=True, null=True)
    testigos = models.ManyToManyField(Testigo, verbose_name=u'Testigos relacionados', blank=True, null=True)
    importante = models.BooleanField()
