#!/usr/bin/env python
#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from abuelas.documentos.models import Documento

class Fiscal(models.Model):
    nombre_apellido = models.CharField("Nombre y Apellido", max_length=70)
    fiscalia = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)
    direccion_fiscalia = models.CharField(max_length=150,blank=True)
    persona_contacto = models.CharField(max_length=150,blank=True)
    email = models.EmailField(blank=True)
    telefonos = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.nombre_apellido + "(" + self.fiscalia + ")"


    class Meta:
        verbose_name_plural = "Fiscales"
        ordering = ['nombre_apellido']

class Querellante(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, blank=True)
    fisica_juridica = models.CharField(max_length=1,choices=(('F', u'Física'),
    ('J', u'Jurídica'),))
    observaciones = models.TextField(blank=True)
    abogado = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido


class Joven(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, blank=True)
    madre = models.CharField(u'Nombre de la madre biológica',
        max_length=100,blank=True)
    padre = models.CharField(u'Nombre del padre biologico',
        max_length=100,blank=True)
    observaciones = models.TextField(blank=True)
    nombre_aprob = models.CharField("Nombre impuesto",
        max_length=50,blank=True)
    fecha_aprop = models.DateField("Fecha de apropiacion",blank=True)
    tipo = models.CharField("Situacion", max_length=50,
        choices=(('APROP', 'Apropiado'),('ADOPT', 'Adoptado'),),)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido


    class Meta:
        verbose_name_plural = u'Jóvenes'

class TipoImputacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True,
    help_text=u'Sé cuidadoso al agregar un nuevo tipo \
            de imputación.Ej: Apropiador, Partícipe, etc.')

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = u'Tipos de imputación'

class Imputado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_imputacion = models.ForeignKey(
        TipoImputacion,
        verbose_name= u'Tipo de imputación', core=True )
    abogado = models.CharField(max_length=50, blank=True)
    mayor70 = models.BooleanField(u'Mayor de 70 años?')
    procesado = models.BooleanField(u'¿Está procesado?')
    observaciones = models.TextField(blank=True)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido

        

class Declaracion(models.Model):
    declarante = models.ForeignKey(Imputado)
    fecha = models.DateField(auto_now=True)
    importante = models.NullBooleanField()
    comentario = models.TextField()

    def __unicode__(self):
        return self.declarante

    class Meta:
        verbose_name_plural = u'Declaraciones'

class Analisis(models.Model):
    joven = models.ForeignKey(Joven)
    tipo = models.CharField(
        max_length=10,
        choices=(
            ('ADN', 'ADN'),
            ('Sangre', 'Sangre'),))
    fecha_realizacion = models.DateField(blank=True)
    resultado = models.TextField(blank=True)

    def __unicode__(self):
        return self.joven + ' (' + self.tipo + ')'


    class Meta:
        pass


class TipoJuzgado(models.Model):
    nombre = models.CharField(max_length=50,help_text=u'Sé cuidadoso \
        al agregar un nuevo tipo de juzgado.Ej: Intrucción, Oral')

    def __unicode__(self):
        return self.nombre


class Juzgado(models.Model):
    nombre_juzgado = models.CharField(u'Nombre y número', max_length=100)
    tipo = models.ForeignKey(TipoJuzgado)
    ciudad = models.CharField(max_length=50)
    juez = models.CharField(u'Juez/ces', max_length=255, blank=True)
    direccion = models.CharField(u'Dirección', max_length=50,blank=True)
    telefonos = models.CharField(u'Teléfonos', max_length=100,blank=True)
    persona_contacto = models.CharField(u'Persona de contacto',
        max_length=100,blank=True)
    email_juzgado = models.EmailField(u'Email de contacto', blank=True)
    observaciones = models.TextField(blank=True)

    def __unicode__(self):
        return self.nombre_juzgado + ' de ' + self.ciudad


class Testigo(models.Model):
    nombre_apellido = models.CharField("Nombre y Apellido", max_length=200)
    observaciones = models.TextField(blank=True)
    


class Caso(models.Model):
    nombre_caso = models.CharField(max_length=100, unique=True)
    caratula = models.CharField(u'Carátula', max_length=100, blank=True,help_text=u'Dejá este campo en blanco si el caso aun no fué presentado')
    juzgado = models.ForeignKey(Juzgado, null=True, blank=True, help_text=u'Dejá este campo en blanco si el caso aun no fué presentado')
    querellante = models.ManyToManyField(Querellante,blank=True)
    fiscal = models.ForeignKey(Fiscal, null=True, blank=True)
    imputados = models.ManyToManyField(Imputado, blank=True)
    joven = models.ManyToManyField(Joven,verbose_name=u"Jóven relacionado/a con la causa",blank=True)
    #punteo = models.TextField(u'Resúmen', null=True, help_text=u'Usá la barra de herramientas para formatear y linkear el texto', blank=True) #wysiwyg
    fecha_ingreso = models.DateTimeField(auto_now_add=True, null=True)  
    observaciones = models.TextField(null=True, blank=True)
    

    def __unicode__(self):
        return self.nombre_caso

