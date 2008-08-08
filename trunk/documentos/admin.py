#! /usr/bin/env python
#coding=utf-8

from django.contrib import admin
from abuelas.documentos.models import Documento

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_upload', 'archivo', 'descripcion')
    list_display_links = ('titulo',)
    list_filter = ('fecha_upload',)
    search_fields = ('titulo', 'descripcion')
    fieldsets = ((None, {'fields': ('archivo','titulo',)}), ('Detalles', {'classes': 'collapse', 'fields': ('descripcion','subido_por')}))

admin.site.register(Documento, DocumentoAdmin)
