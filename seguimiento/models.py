#!/usr/bin/env python
#coding=utf-8

from django.db import models
from django.contrib.auth.models import User


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


    class Admin:
        list_display = ('nombre_apellido', 'fiscalia', 'telefonos')
        list_filter = ('nombre_apellido', 'fiscalia')
        search_fields = ['nombre_apellido', 'fiscalia', '@observaciones']


        fields = ((None, {'fields': ('nombre_apellido', 'fiscalia',
                    'observaciones')}),
                    ('Informacion de contacto',
                    {'classes': 'collapse','fields':
                    ('direccion_fiscalia', 'persona_contacto',
                    'email', 'telefonos')}),)

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

    class Admin:
        pass

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
        choices=(('APROP', 'Apropiado'),('ADOPT', 'Adoptado'),),
        radio_admin=True)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido

    class Admin:
        pass

    class Meta:
        verbose_name_plural = u'Jóvenes'

class TipoImputacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True,
    help_text=u'Sé cuidadoso al agregar un nuevo tipo \
            de imputación.Ej: Apropiador, Partícipe, etc.')

    def __unicode__(self):
        return self.nombre

    class Admin:
        pass

    class Meta:
        verbose_name_plural = u'Tipos de imputación'

class RolParticipacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True,
        help_text=u'Sé cuidadoso al agregar un rol. Ej: Médico, Partera... ')

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = u'Roles de participación'

    class Admin:
        pass

class Imputado(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, blank=True)
    tipo_imputacion = models.ForeignKey(
        TipoImputacion,
        verbose_name= u'Tipo de imputación', core=True, edit_inline=True)
    rol = models.ForeignKey(RolParticipacion, verbose_name=u'Rol en el hecho', core=True, edit_inline=True)
    abogado = models.CharField(max_length=50, blank=True)
    mayor70 = models.BooleanField(u'Mayor de 70 años?')
    procesado = models.BooleanField(u'¿Está procesado?')
    observaciones = models.TextField(blank=True)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido

    class Admin:
        pass

class Declaracion(models.Model):
    declarante = models.ForeignKey(Imputado)
    fecha = models.DateField(auto_now=True)
    importante = models.NullBooleanField()
    comentario = models.TextField()

    def __unicode__(self):
        return self.declarante + ' ' + repr(fecha)

    class Meta:
        verbose_name_plural = u'Declaraciones'

    class Admin:
        pass

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

    class Admin:
        pass

    class Meta:
        pass


class TipoJuzgado(models.Model):
    nombre = models.CharField(max_length=50,help_text=u'Sé cuidadoso \
        al agregar un nuevo tipo de juzgado.Ej: Intrucción, Oral')

    def __unicode__(self):
        return self.nombre

    class Admin:
        pass


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

    class Admin:

        fields = ((None,
            {'fields':('nombre_juzgado','tipo','ciudad',
                'juez','observaciones')}),
                    ('Informacion de contacto',{
                            'classes': 'collapse',
                                'fields': ('direccion', 'persona_contacto',
                                'telefonos', 'email_juzgado')}),
                )



class Caso(models.Model):
    nombre_caso = models.CharField(max_length=100)
    caratula = models.CharField(u'Carátula', max_length=100, blank=True,help_text=u'Dejá este campo en blanco si el caso aun no fué presentado')
    juzgado = models.ForeignKey(Juzgado, null=True, blank=True, help_text=u'Dejá este campo en blanco si el caso aun no fué presentado')
    querellante = models.ManyToManyField(Querellante,blank=True, filter_interface=models.HORIZONTAL)
    fiscal = models.ForeignKey(Fiscal, null=True, blank=True)
    imputados = models.ManyToManyField(Imputado, blank=True, filter_interface=models.HORIZONTAL)
    joven = models.ManyToManyField(Joven,verbose_name=u"Jóven relacionado/a con la causa",blank=True, filter_interface=models.HORIZONTAL)
    #punteo = models.TextField(u'Resúmen', null=True, help_text=u'Usá la barra de herramientas para formatear y linkear el texto', blank=True) #wysiwyg
    fecha_ingreso = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.nombre_caso

    class Admin:
        js = ('/datos/js/jquery/jquery.js',
            '/datos/js/wymeditor/jquery.wymeditor.js',
            '/datos/js/admin_textarea.js')

        list_display = ('nombre_caso','caratula', 'juzgado', 'fiscal')
        list_display_links = ('nombre_caso','caratula')
        list_filter = ('querellante', 'fiscal', 'juzgado',)
        search_fields = ['caratula', 'nombre_caso', '@resumen']
        fields = ((None, {'fields': ('nombre_caso', 'caratula', 'juzgado',)}),
                        ('Detalles', {'classes': 'collapse','fields': ('fiscal', 'querellante','imputados', 'joven', 'punteo')}))

class ParrafoPunteo(models.Model):
    caso = models.ForeignKey(Caso)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User)
    texto = models.TextField()

    def __unicode__(self):
        return texto

    class Admin:
        pass


class Testigo(models.Model):
    nombre_apellido = models.CharField("Nombre y Apellido", max_length=200)
    observaciones = models.TextField(blank=True)
    


class CategoriaMarcasPunteo(models.Model):
    nombre = models.CharField(u'Categoría de marcas de punteo', max_length=100, unique=True)
    
    def __unicode__(self):
         return self.nombre
    
    class Meta:
        verbose_name_plural = u'Categorías de marcas de punteo'
    
    class Admin:
        pass
    
class MarcasPunteo(models.Model):
    causa = models.ForeignKey(Caso)
    parrafo = models.ForeignKey(ParrafoPunteo)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User)
    categoria = models.ForeignKey(CategoriaMarcasPunteo)
    fecha_incidente = models.DateField(u'Fecha relacionada', blank=True, null=True)
    comentario = models.TextField(u'Comentario')
    imputados = models.ManyToManyField(Imputado, verbose_name=u'Imputados relacionados', blank=True, null=True)
    testigos = models.ManyToManyField(Testigo, verbose_name=u'Testigos relacionados', blank=True, null=True)
    importante = models.BooleanField()
    

class Incidente(models.Model):
    nombre_caso_padre = models.ForeignKey(Caso)
    nombre_caso = models.CharField(max_length=100)
    caratula = models.CharField(max_length=100, blank=True)
    etapaJudicial = models.CharField("Etapa del proceso", max_length=5, choices=(('INV', u'Investigación'),('INS', u'Intrucción'),('JO', u'Juicio Oral'),('AP', u'Apelación')))
    juzgado = models.ForeignKey(Juzgado)

    def __unicode__(self):
        return self.nombre_caso

    class Admin:
        pass


class CategoriaSeguimiento(models.Model):
    nombre = models.CharField(u'Categoría de seguimiento', max_length=100, unique=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = u'Categorías de seguimiento'

    class Admin:
        pass


class Seguimiento(models.Model):
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User)	
    categoria = models.ForeignKey(CategoriaSeguimiento)
    causa = models.ForeignKey(Caso)
    foja = models.CharField(max_length=20) 
    importante = models.BooleanField()
    comentario = models.TextField()

    def __unicode__(self):
        return "seguimiento " + str(self.fecha_ingreso)

    class Admin:
        list_display = ('fecha_ingreso','creado_por', 'causa', 'foja', 'comentario')
        list_display_links = ('fecha_ingreso', 'causa')
        list_filter = ('causa','fecha_ingreso','categoria', 'creado_por')        
        ordering = ['fecha_ingreso','causa']

    class Meta:
        order_with_respect_to = 'causa'

class SeguimientoIncidente(models.Model):
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User)
    incidente = models.ForeignKey(Incidente)
    foja = models.CharField(max_length=20)
    comentario = models.TextField()

    def __unicode__(self):
        return "seguimiento Incidente" + str(self.fecha_ingreso)

    class Admin:
        date_hierarchy = 'fecha_ingreso'
        fields = ((None, {'fields': (('fecha_ingreso', 'foja'),
            ('incidente','creado_por'), 'comentario',)}),
            ('Opciones avanzadas', {'classes': 'collapse','fields': 
            ('vencimiento', )}),)