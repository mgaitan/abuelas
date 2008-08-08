#! /usr/bin/env python
#coding=utf-8

from django.contrib import admin
from abuelas.seguimiento.models import *

class GenericAdmin(admin.ModelAdmin):
    pass

admin.site.register(CategoriaSeguimiento, GenericAdmin)

class SeguimientoAdmin(admin.ModelAdmin):
    class Media:
        js = ('/datos/js/rte.jquery/jquery.js',
           '/datos/js/rte.jquery/jquery.rte.js',
           '/datos/js/rte.jquery/admin_textarea.js')        
    list_display = ('fecha_ingreso','creado_por', 'causa', 'foja', 'comentario', 'vencimiento')
    list_display_links = ('fecha_ingreso', 'causa')
    list_filter = ('causa','fecha_ingreso','categoria', 'creado_por')        
    ordering = ['fecha_ingreso','causa']
    fieldsets = ((None, {'fields': ('categoria', 'foja', 'comentario','vencimiento',)}),
                            ('Detalles', {'classes': 'collapse','fields': ('creado_por', 'causa')}))

admin.site.register(Seguimiento, SeguimientoAdmin)

class SeguimientoIncidenteAdmin(admin.ModelAdmin):
    pass
    #date_hierarchy = ['fecha_ingreso',]
    #fieldsets = ((None, {'fields': (('fecha_ingreso', 'foja'),
    #    ('incidente','creado_por'), 'comentario',)}),
    #    ('Opciones avanzadas', {'classes': 'collapse','fields': 
    #    ('vencimiento', )}),)
        
        
admin.site.register(SeguimientoIncidente, SeguimientoIncidenteAdmin)

        