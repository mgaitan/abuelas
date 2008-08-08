#! /usr/bin/env python
#coding=utf-8


from django.contrib import admin
from abuelas.casos.models import *

class FiscalAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('nombre_apellido', 'fiscalia',
                 'observaciones')}),
                 ('Informacion de contacto',
                 {'classes': 'collapse','fields':
                 ('direccion_fiscalia', 'persona_contacto',
                 'email', 'telefonos')}),)
    list_display = ('nombre_apellido', 'fiscalia', 'telefonos')
    list_filter = ('nombre_apellido', 'fiscalia')
    search_fields = ['nombre_apellido', 'fiscalia', '@observaciones']

admin.site.register(Fiscal, FiscalAdmin)

class GenericAdmin(admin.ModelAdmin):
    pass


admin.site.register(Joven, GenericAdmin)
admin.site.register(Querellante, GenericAdmin)
admin.site.register(TipoImputacion, GenericAdmin)
admin.site.register(Declaracion, GenericAdmin)
admin.site.register(Analisis, GenericAdmin)
admin.site.register(TipoJuzgado, GenericAdmin)
admin.site.register(Testigo, GenericAdmin)


class ImputadoAdmin(admin.ModelAdmin):
    class Media:
        js = ('/datos/js/rte.jquery/jquery.js',
              '/datos/js/rte.jquery/jquery.rte.js',
              '/datos/js/rte.jquery/admin_textarea.js')        
    
    list_filter = ('tipo_imputacion', 'procesado', 'mayor70') 
    search_fields = ('nombre', 'apellido', 'observaciones')
    

admin.site.register(Imputado, ImputadoAdmin)

class JuzgadoAdmin(admin.ModelAdmin):
    fieldsets = ((None,
        {'fields':('nombre_juzgado','tipo','ciudad',
            'juez','observaciones')}),
                ('Informacion de contacto',{
                        'classes': 'collapse',
                            'fields': ('direccion', 'persona_contacto',
                            'telefonos', 'email_juzgado')}),
            )

admin.site.register(Juzgado, JuzgadoAdmin)

class CasoAdmin(admin.ModelAdmin):
    class Media:
        js = ('/datos/js/rte.jquery/jquery.js',
           '/datos/js/rte.jquery/jquery.rte.js',
           '/datos/js/rte.jquery/admin_textarea.js')        

    list_display = ('nombre_caso','caratula', 'juzgado', 'fiscal')
    list_display_links = ('nombre_caso','caratula')
    list_filter = ('querellante', 'fiscal', 'juzgado')
    search_fields = ('nombre_caso',)

    fieldsets = ((None, {'fields': ('nombre_caso', 'caratula', 'juzgado','observaciones',)}),
                    ('Detalles', {'classes': 'collapse','fields': ('fiscal', 'querellante','imputados', 'joven')}))


admin.site.register(Caso, CasoAdmin)
