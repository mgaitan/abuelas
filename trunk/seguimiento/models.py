# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Persona(models.Model):

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido
        
	class Admin:
		pass

    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50)
    alias = models.SlugField(blank=True)
    sexo = models.CharField(maxlength=1,choices=(('M', 'Masculino'),('F', 'Femenino'),), radio_admin=True)
    observaciones = models.TextField(blank=True)
    ocupacion = models.CharField(maxlength=50, default='Abogado', editable=False)

class Abogado(models.Model):
    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50)
    observaciones = models.TextField(blank=True)
    ocupacion = models.CharField(maxlength=50, default='Abogado', editable=False)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido
    
    class Admin:
        pass
    
       
class Fiscal(models.Model):
    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50)
    observaciones = models.TextField(blank=True)
    fiscalia = models.CharField(maxlength=100)
    direccion_fiscalia =  models.CharField(maxlength=150)
    telefonos = models.SlugField(blank=True)

    def __unicode__(self):
        return self.nombre + ' ' + self.apellido
            
    class Admin:
        pass

class Querellante(models.Model):
    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50, blank=True)
    fisicaOjuridica = models.CharField(maxlength=1,choices=(('F', u'Física'),('J', u'Jurídica'),))
    observaciones = models.TextField(blank=True)
    abogado = models.ManyToManyField(Abogado)
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
    mayor70 = models.BooleanField(u'Mayor de 70 años?')
    procesado = models.BooleanField(u'¿Está procesado?')
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

class EtapaJudicial(models.Model):
    nombre = models.CharField(maxlength=100)
    tipoFuero = models.CharField(maxlength=50,choices=(('Penal', 'Penal'),('Apelacion', u'Apelacion'),) )
    ciudad = models.CharField(maxlength=50)
    direccion = models.CharField(maxlength=50,blank=True)
    telefonos = models.SlugField(blank=True)
    personaContacto = models.CharField(maxlength=100,blank=True)

    def __unicode__(self):
   	    return self.nombre + ' de ' + self.ciudad

    class Admin:
        pass

   

class Causa(models.Model):
	caso = models.CharField(maxlength=100)
   	caratula = models.CharField(maxlength=100,blank=True)
   	joven = models.ManyToManyField(Joven,verbose_name=u"Jóven relacionado/a con la causa",blank=True)
   	etapaJudicial = models.ForeignKey(EtapaJudicial)
   	fiscal = models.ForeignKey(Fiscal)
   	imputados = models.ManyToManyField(Imputado, blank=True)
   	punteo = models.TextField("Resumen de la causa", help_text="Puede usar codigo HTML para formatear y linkear su texto")
   	#observaciones = models.TextField(blank=True)

   	def __unicode__(self):
   		return self.caso
    
	class Admin:
		js = ('/datos/js/jquery/jquery.js',
			'/datos/js/wymeditor/jquery.wymeditor.js',
			'/datos/js/admin_textarea.js')
		

class Incidente(models.Model):    
    caso_padre = models.ForeignKey(Causa)
    caso = models.CharField(maxlength=100)
    caratula = models.CharField(maxlength=100, blank=True)
    etapaJudicial = models.ForeignKey(EtapaJudicial) 
    
    def __unicode__(self):
        return self.caso   	    

    class Admin:
        pass


class Evento(models.Model):
    fecha_vencimiento = models.DateTimeField()
    asunto = models.CharField(maxlength=200)

	
    def __unicode__(self):
	    return "evento " + str(self.fecha_vencimiento)

    class Admin:
	    pass


class Seguimiento(models.Model):
	fecha_ingreso = models.DateTimeField(auto_now_add=True)
	creado_por = models.ForeignKey(User)
	causa = models.ForeignKey(Causa)
	#autor = models.ForeignKey(Usuario)
	vencimiento = models.ForeignKey(Evento, blank=True)
	foja = models.CharField(maxlength=20)
	titulo = models.CharField(maxlength=100, blank=True)
	comentario = models.TextField()

	def __unicode__(self):
		pass

	class Admin:
		pass



class SeguimientoIncidente(models.Model):
	fecha_ingreso = models.DateTimeField(auto_now_add=True)
	creado_por = models.ForeignKey(User)
	Incidente = models.ForeignKey(Incidente)
	#autor = models.ForeignKey(Usuario)
	fecha_vencimiento = models.ForeignKey(Evento, blank=True)
	foja = models.CharField(maxlength=20)
	comentario = models.TextField()

   	def __unicode__(self):
   	    return "seguimiento " + str(self.fecha_ingreso)

	class Admin:
		pass



