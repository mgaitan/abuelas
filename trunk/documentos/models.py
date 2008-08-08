#!/usr/bin/env python
#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

PATH_ARCHIVOS = '%Y/%m/%d'


class Documento(models.Model):
    archivo = models.FileField("Archivo", upload_to=PATH_ARCHIVOS)
    titulo = models.CharField(u'Título', unique=True, max_length=50, help_text=u'Ingresa un título breve para este documento')
    descripcion = models.TextField(u'Descripción', null=True, blank=True)
    subido_por = models.ForeignKey(User, null=True, blank=True)
    fecha_upload = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return self.titulo