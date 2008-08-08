#! /usr/bin/env python
#coding=utf-8

from django.contrib import admin
from abuelas.punteo.models import *

class GenericAdmin(admin.ModelAdmin):
    pass

class PunteoAdmin(admin.ModelAdmin):
    class Media:
         js = ('/datos/js/rte.jquery/jquery.js',
                '/datos/js/rte.jquery/jquery.rte.js',
                '/datos/js/rte.jquery/admin_textarea.js')
    list_display = ('fecha_ingreso', 'caso', 'creado_por', 'texto')
    list_display_links = ('fecha_ingreso',)
    list_filter = ('caso','fecha_ingreso','creado_por')        
    ordering = ['fecha_ingreso','caso']        
    fieldsets = ((None, {'fields': ('texto', 'adjuntos')}),
                         ('Detalles', {'classes': 'collapse','fields': ('creado_por', 'caso')}))

    

admin.site.register(ParrafoPunteo, PunteoAdmin)
admin.site.register(CategoriaMarcasPunteo, GenericAdmin)
admin.site.register(MarcasPunteo, GenericAdmin)


