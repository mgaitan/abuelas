# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

       
class Fiscal(models.Model):
    nombreApellido = models.CharField("Nombre y Apellido", maxlength=70)
    fiscalia = models.CharField(maxlength=100)
    observaciones = models.TextField(blank=True)
    direccion_fiscalia = models.CharField(maxlength=150,blank=True)
    personaContacto = models.CharField(maxlength=150,blank=True)
    email = models.EmailField(blank=True)
    telefonos = models.CharField(maxlength=50, blank=True)

    def __unicode__(self):
        return self.nombreApellido + "(" + self.fiscalia + ")"
            
    class Admin:
        list_display = ('nombreApellido', 'fiscalia', 'telefonos')
        list_filter = ('nombreApellido', 'fiscalia')
        search_fields = ['nombreApellido', 'fiscalia', '@observaciones']
        
    class Meta:        
        verbose_name_plural = "Fiscales"
        ordering = ['nombreApellido']        

class Querellante(models.Model):
    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50, blank=True)
    fisicaOjuridica = models.CharField(maxlength=1,choices=(('F', u'Física'),('J', u'Jurídica'),))
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
    nombreAprop = models.CharField("Nombre impuesto", maxlength=50,blank=True)
    fechaAprop = models.DateField("Fecha de apropiacion",blank=True)
    tipo = models.CharField("Situacion", maxlength=50, choices=(('APROP', 'Apropiado'),('ADOPT', 'Adoptado'),), radio_admin=True)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido

    class Admin:
        pass


    
class Imputado(models.Model):
    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50, blank=True)
    tipoImputacion = models.CharField("Tipo de imputacion", maxlength=50, choices=(('apropiacion', u'Apropiación'),('participacion', u'Participación'),('Otro', 'Otro')))
    rolImputacion = models.CharField("Rol de imputacion", maxlength=50, choices=(('apropiador', 'Apropiador'),('medico', u'Médico'),('Enfermera', u'Enfermera')))
    abogado = models.CharField(maxlength=50, blank=True)
    mayor70 = models.BooleanField(u'Mayor de 70 años?')
    procesado = models.BooleanField(u'¿Está procesado?')
    observaciones = models.TextField(blank=True)    
    declaro  =  models.CharField("Tipo de imputacion", maxlength=50, choices=(('apropiacion', u'Apropiación'),('participacion', u'Participación'),('Otro', 'Otro')))
    def __unicode__(self):
        return self.nombre + ' ' + self.apellido

    
    class Admin:
        pass


    
    


class Analisis(models.Model):
    joven = models.ForeignKey(Joven)
    tipo = models.CharField(maxlength=10,choices=(('ADN', 'ADN'),('Sangre', 'Sangre'),) )
    fecha_realizacion = models.DateField(blank=True)
    resultado = models.TextField(blank=True)

    def __unicode__(self):
        return 'Analisis tipo' + tipo 
        
    class Admin:
        pass

class Juzgado(models.Model):
    nombreJuzgado = models.CharField(u'Nombre y número', maxlength=100)
    ciudad = models.CharField(maxlength=50)
    juez = models.CharField(u'Juez/ces', maxlength=150, blank=True)
    direccion = models.CharField(u'Dirección', maxlength=50,blank=True)
    telefonos = models.CharField(u'Teléfonos', maxlength=100,blank=True)
    personaContacto = models.CharField(u'Persona de contacto', maxlength=100,blank=True)    
    emailJuzgado  = models.EmailField(u'Email de contacto', blank=True)
    observaciones = models.TextField(blank=True)

    def __unicode__(self):
   	    return self.nombreJuzgado + ' de ' + self.ciudad

    class Admin:
		fields = ((None, {
				'fields': ('nombreJuzgado', 'ciudad','juez', 'observaciones')}),
            ('Informacion de contacto', {
                'classes': 'collapse',
                'fields' : ('direccion', 'personaContacto', 'telefonos', 'emailJuzgado')
            }),
       			)    	


   

class Causa(models.Model):
	caso = models.CharField(maxlength=100)
   	caratula = models.CharField(maxlength=100,blank=True)
   	etapaJudicial = models.CharField("Etapa del proceso", maxlength=100, choices=(('INV', u'Investigación'),('INS', u'Intrucción'),('JO', u'Juicio Oral'),('AP', u'Apelación')))
   	juzgado = models.ForeignKey(Juzgado, null=True, blank=True)
   	querellante = models.ForeignKey(Querellante, null=True, blank=True)
   	abuelas_presentado = models.NullBooleanField(u'¿Abuelas es parte?')
   	fiscal = models.ForeignKey(Fiscal, null=True, blank=True)
   	punteo = models.TextField(u'Resúmen', help_text="Puede usar codigo HTML para formatear y linkear su texto", blank=True) #wysiwyg
   	imputados = models.ManyToManyField(Imputado, blank=True)
   	joven = models.ManyToManyField(Joven,verbose_name=u"Jóven relacionado/a con la causa",blank=True)   	


   	def __unicode__(self):
   		return self.caso
    
	class Admin:
		js = ('/datos/js/jquery/jquery.js',
			'/datos/js/wymeditor/jquery.wymeditor.js',
			'/datos/js/admin_textarea.js')

		list_display = ('caso','caratula', 'etapaJudicial', 'juzgado', 'querellante')
		list_display_links = ('caso','caratula')
		list_filter = ('etapaJudicial', 'querellante', 'fiscal', 'juzgado','abuelas_presentado', )
        search_fields = ['caratula', 'caso', '@punteo']


        fields = ((None, {'fields': ('caso', 'caratula', 'etapaJudicial',)}),
                ('Detalles', {'classes': 'collapse','fields' : ('juzgado', 'fiscal', ('querellante','abuelas_presentado'), ('imputados', 'joven',), ) }),
                ('Punteo', {'classes': 'collapse','fields' : ('punteo')}),)

class Incidente(models.Model):    
    caso_padre = models.ForeignKey(Causa)
    caso = models.CharField(maxlength=100)
    caratula = models.CharField(maxlength=100, blank=True)
    etapaJudicial = models.CharField("Etapa del proceso", maxlength=5, choices=(('INV', u'Investigación'),('INS', u'Intrucción'),('JO', u'Juicio Oral'),('AP', u'Apelación')))
    juzgado = models.ForeignKey(Juzgado)
    
    def __unicode__(self):
        return self.caso   	    

    class Admin:
        pass



class Seguimiento(models.Model):
	fechaIngreso = models.DateTimeField(auto_now_add=True)
	creadoPor = models.ForeignKey(User)	
	causa = models.ForeignKey(Causa)
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


