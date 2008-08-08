#!/usr/bin/env python
#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from abuelas.casos.models import Caso, Documento, Juzgado



class Incidente(models.Model):
    nombre_caso_padre = models.ForeignKey(Caso)
    nombre_caso = models.CharField(max_length=100)
    caratula = models.CharField(max_length=100, blank=True)
    etapaJudicial = models.CharField("Etapa del proceso", max_length=5, choices=(('INV', u'Investigación'),('INS', u'Intrucción'),('JO', u'Juicio Oral'),('AP', u'Apelación')))
    juzgado = models.ForeignKey(Juzgado)

    def __unicode__(self):
        return self.nombre_caso

