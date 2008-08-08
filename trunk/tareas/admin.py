#! /usr/bin/env python
#coding=utf-8

from django.contrib import admin
from abuelas.tareas.models import *

class GenericAdmin(admin.ModelAdmin):
    pass

admin.site.register(Proyecto, GenericAdmin)

class TareaAdmin(admin.ModelAdmin):
    list_filter = ('proyecto', 'prioridad', 'vencimiento', 'asignado', 'completado')
    search_fields = ['@descripcion', '@comentario']
    list_display = ('fechaCreacion','prioridad', 'proyecto', 'descripcion', 'completado')

admin.site.register(Tarea, TareaAdmin)
