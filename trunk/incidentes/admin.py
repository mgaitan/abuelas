#! /usr/bin/env python
#coding=utf-8

from django.contrib import admin
from abuelas.incidentes.models import *

class GenericAdmin(admin.ModelAdmin):
    pass

admin.site.register(Incidente, GenericAdmin)
