# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

       
class Fiscal(models.Model):
    nombre_apellido = models.CharField("Nombre y Apellido", maxlength=70)
    fiscalia = models.CharField(maxlength=100)
    observaciones = models.TextField(blank=True)
    direccion_fiscalia = models.CharField(maxlength=150,blank=True)
    persona_contacto = models.CharField(maxlength=150,blank=True)
    email = models.EmailField(blank=True)
    telefonos = models.CharField(maxlength=50, blank=True)

    def __unicode__(self):
        return self.nombre_apellido + "(" + self.fiscalia + ")"
            
    class Admin:
        list_display = ('nombre_apellido', 'fiscalia', 'telefonos')
        list_filter = ('nombre_apellido', 'fiscalia')
        search_fields = ['nombre_apellido', 'fiscalia', '@observaciones']
        
    class Meta:        
        verbose_name_plural = "Fiscales"
        ordering = ['nombre_apellido']        

class Querellante(models.Model):
    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50, blank=True)
    fisica_juridica = models.CharField(maxlength=1,choices=(('F', u'Física'),('J', u'Jurídica'),))
    observaciones = models.TextField(blank=True)
    abogado = models.CharField(maxlength=50, blank=True)
    def __unicode__(self):
        return self.nombre + ' ' + self.apellido
    class Admin:
        pass

class Joven(models.Model):
    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50, blank=True)
    madre = models.CharField(u'Nombre de la madre biológica', maxlength=100,blank=True)
    padre = models.CharField(u'Nombre del padre biologico', maxlength=100,blank=True)
    observaciones = models.TextField(blank=True)    
    nombre_aprob = models.CharField("Nombre impuesto", maxlength=50,blank=True)
    fecha_aprop = models.DateField("Fecha de apropiacion",blank=True)
    tipo = models.CharField("Situacion", maxlength=50, choices=(('APROP', 'Apropiado'),('ADOPT', 'Adoptado'),), radio_admin=True)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido

    class Admin:
        pass

    class Meta:        
        verbose_name_plural = u'Jóvenes'


class TipoImputacion(models.Model):
	nombre = models.CharField(maxlength=100, unique=True, help_text=u'Sé cuidadoso al agregar un nuevo tipo de imputación.Ej: Apropiador, Partícipe, etc.')

	def __unicode__(self):
		return self.nombre

	class Admin:
		pass

	class Meta:
		verbose_name_plural = u'Tipos de imputación'	

class RolParticipacion(models.Model):
    nombre = models.CharField(maxlength=50, unique=True, help_text=u'Sé cuidadoso al agregar un rol. Ej: Médico, Partera, etc')
    
    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = u'Roles de participación'

    class Admin:
        pass    

   
    
class Imputado(models.Model):
    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50, blank=True)
    tipo_imputacion = models.ForeignKey(TipoImputacion, verbose_name= u'Tipo de imputación')
    rol = models.ForeignKey(RolParticipacion, verbose_name=u'Rol en el hecho')
    abogado = models.CharField(maxlength=50, blank=True)
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
    tipo = models.CharField(maxlength=10,choices=(('ADN', 'ADN'),('Sangre', 'Sangre'),) )
    fecha_realizacion = models.DateField(blank=True)
    resultado = models.TextField(blank=True)

    def __unicode__(self):
        return self.joven + ' (' + self.tipo + ')'
        
    class Admin:
        pass

    class Meta:        
        verbose_name_plural = u'Análisis'


class TipoJuzgado(models.Model):
    nombre = models.CharField(maxlength=50, help_text=u'Sé cuidadoso al agregar un nuevo tipo de juzgado. Ej: Intrucción, Oral')
    
    def __unicode__(self):
        return self.nombre

    class Admin:
        pass  


class Juzgado(models.Model):
    nombre_juzgado = models.CharField(u'Nombre y número', maxlength=100)
    tipo = models.ForeignKey(TipoJuzgado)
    ciudad = models.CharField(maxlength=50)
    juez = models.CharField(u'Juez/ces', maxlength=255, blank=True)
    direccion = models.CharField(u'Dirección', maxlength=50,blank=True)
    telefonos = models.CharField(u'Teléfonos', maxlength=100,blank=True)
    persona_contacto = models.CharField(u'Persona de contacto', maxlength=100,blank=True)    
    email_juzgado  = models.EmailField(u'Email de contacto', blank=True)
    observaciones = models.TextField(blank=True)

    def __unicode__(self):

		return self.nombre_juzgado + ' de ' + self.ciudad

    class Admin:

		fields = ((None, {
				'fields': ('nombre_juzgado', 'tipo', 'ciudad','juez', 'observaciones')}),
            ('Informacion de contacto', {
                'classes': 'collapse',
                'fields' : ('direccion', 'persona_contacto', 'telefonos', 'email_juzgado')
            }),
       			)    	


   

class Caso(models.Model):
	nombre_caso = models.CharField(maxlength=100)
	caratula = models.CharField(u'Carátula', maxlength=100,blank=True,help_text=u'Dejá este campo en blanco si el caso aun no fué presentado' )
	juzgado = models.ForeignKey(Juzgado, null=True, blank=True, help_text=u'Dejá este campo en blanco si el caso aun no fué presentado')
	querellante = models.ForeignKey(Querellante, null=True, blank=True)
	fiscal = models.ForeignKey(Fiscal, null=True, blank=True)
	imputados = models.ManyToManyField(Imputado, blank=True)
	joven = models.ManyToManyField(Joven,verbose_name=u"Jóven relacionado/a con la causa",blank=True)   	
	punteo = models.TextField(u'Resúmen', help_text=u'Usá la barra de herramientas para formatear y linkear el texto', blank=True) #wysiwyg


   	def __unicode__(self):
   		return self.nombre_caso

	class Admin:
		js = ('/datos/js/jquery/jquery.js',
			'/datos/js/wymeditor/jquery.wymeditor.js',
			'/datos/js/admin_textarea.js')

		list_display = ('nombre_caso','caratula', 'juzgado', 'querellante')
		list_display_links = ('nombre_caso','caratula')
		list_filter = ('querellante', 'fiscal', 'juzgado',)
		search_fields = ['caratula', 'nombre_caso', '@resumen']


        fields = ((None, {'fields': ('nombre_caso', 'caratula', 'juzgado',)}),
                ('Detalles', {'classes': 'collapse','fields' : ('fiscal', 'querellante','imputados', 'joven',) }),
                ('Punteo', {'classes': 'collapse','fields' : ('punteo')}),)

class Incidente(models.Model):    
    nombre_caso_padre = models.ForeignKey(Caso)
    nombre_caso = models.CharField(maxlength=100)
    caratula = models.CharField(maxlength=100, blank=True)
    etapaJudicial = models.CharField("Etapa del proceso", maxlength=5, choices=(('INV', u'Investigación'),('INS', u'Intrucción'),('JO', u'Juicio Oral'),('AP', u'Apelación')))
    juzgado = models.ForeignKey(Juzgado)
    
    def __unicode__(self):
        return self.nombre_caso   	    

    class Admin:
        pass


class CategoriaSeguimiento(models.Model):
    nombre = models.CharField(u'Categoría de seguimiento', maxlength=100, unique=True)
    
    def __unicode__(self):
        return self.nombre

	class Meta:        
		verbose_name_plural = u'Categorías de seguimiento'

	class Admin:
		pass




class Seguimiento(models.Model):
	fechaIngreso = models.DateTimeField(auto_now_add=True)
	creado_por = models.ForeignKey(User)	
	categoria = models.ForeignKey(CategoriaSeguimiento)
	causa = models.ForeignKey(Caso)
	foja = models.CharField(maxlength=20)
	comentario = models.TextField()

	def __unicode__(self):
		return "seguimiento " + str(self.fecha_ingreso)

	class Admin:

		fields = (
            (None, {'fields': (('fechaIngreso', 'foja'), ('incidente','creadoPor'), 'comentario',)
            }),
			('Opciones avanzadas', {
                'classes': 'collapse',
                'fields' : ('vencimiento', )
            }),
        )    	

        list_display = ('fechaIngreso','creadoPor', 'causa', 'foja', 'comentario')
        list_display_links = ('fechaIngreso', 'causa')
        list_filter = ('causa','fechaIngreso','creadoPor')    
        ordering = ['fechaIngreso','causa']


	class Meta:
		order_with_respect_to = 'causa'



class SeguimientoIncidente(models.Model):
	fechaIngreso = models.DateTimeField(auto_now_add=True)
	creadoPor = models.ForeignKey(User)
	incidente = models.ForeignKey(Incidente)
	foja = models.CharField(maxlength=20)
	comentario = models.TextField()

   	def __unicode__(self):
   	    return "seguimiento Incidente" + str(self.fecha_ingreso)

	class Admin:
		date_hierarchy = 'fechaIngreso'

		fields = ((None, {
				'fields': (('fechaIngreso', 'foja'), ('incidente','creadoPor'), 'comentario',)}),
            ('Opciones avanzadas', {
                'classes': 'collapse',
                'fields' : ('vencimiento', )
            }),
       			)    	

