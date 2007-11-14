from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Persona(models.Model):
    SEXO_OPCIONES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),       
    )
    nombre = models.CharField(maxlength=50)
    apellido = models.CharField(maxlength=50)
    alias = models.SlugField(blank=True)
    ocupacion = models.CharField(maxlength=50)
    sexo = models.CharField(maxlength=1,choices=SEXO_OPCIONES, radio_admin=True)
    observaciones = models.TextField(blank=True)
    def __unicode__(self):
        return self.nombre + ' ' + self.apellido

	class Admin:
		pass


class Abogado(Persona):
    ocupacion = models.CharField(maxlength=50, default='Abogado', editable=False)

    def lala(self):
        pass
    
    class Admin:
        pass
    
class Juez(Persona):
    ocupacion = models.CharField(maxlength=50, default='Juez', editable=False)
    def lala(self):
        pass
    class Admin:
        pass
        
class Fiscal(Persona):
    ocupacion = models.CharField(maxlength=50, default='Fiscal', editable=False)
    fiscalia = models.CharField(maxlength=100)
    direccion_fiscalia =  models.CharField(maxlength=150)
    telefonos = models.SlugField(blank=True)

    def lala(self):
        pass
            
    class Admin:
        pass


class Querellante(Persona):
    abogado = models.ManyToManyField(Abogado)
    def __unicode__(self):
        return "querellante: " + self.nombre + ' ' + self.apellido

    class Admin:
        pass



class Joven(Persona):
    madre = models.CharField("Nombre de la madre biologica", maxlength=100,blank=True)
    padre = models.CharField("Nombre del padre biologico", maxlength=100,blank=True)
    nombreAprop = models.CharField("Nombre impuesto", maxlength=50,blank=True)
    fechaAprop = models.DateField("Fecha de apropiacion",blank=True)
    tipo = models.CharField("Situacion", maxlength=50, choices=(('APROP', 'Apropiado'),('ADOPT', 'Adoptado'),), radio_admin=True)
    def __unicode__(self):
        return self.nombre + ' ' + self.apellido

    class Admin:
        pass
    
class Imputado(Persona):
    tipoImputacion = models.CharField("Tipo de imputacion", maxlength=50, choices=(('Apropiacion', 'Apropiacion'),('Participe', 'Participe Necesario'),('Otro', 'Otro')))
    rolImputacion = models.CharField("Rol de imputacion", maxlength=50, choices=(('Apropiador', 'Apropiador'),('Medico', 'Medico'),('Enfermera', 'Enfermera')))
    mayor70 = models.BooleanField("Mayor de 70?")
    procesado = models.BooleanField("Esta procesado?")
    def __unicode__(self):
        return "imputado: " + self.nombre + ' ' + self.apellido

    

    class Admin:
        pass

    


class Analisis(models.Model):
    joven = models.OneToOneField(Joven)
    tipo = models.CharField(maxlength=10,choices=(('ADN', 'ADN'),('Sangre', 'Sangre'),) )
    fecha_realizacion = models.DateField(blank=True)
    resultado = models.TextField(blank=True)

    def __unicode__(self):
        return 'Analisis tipo' + tipo 
        
    class Admin:
        pass

class EtapaJudicial(models.Model):
    instancia = models.CharField(maxlength=50,choices=(('Juzgado', 'Juzgado'),('Tribunal', 'Tribunal'),) )
    tipo_fuero = models.CharField(maxlength=50,choices=(('Penal', 'Penal'),('Apelacion', 'Apelacion'),) )
    numero = models.CharField(maxlength=10)
    ciudad = models.CharField(maxlength=50)
    conocido_como = models.CharField(maxlength=50,blank=True)
    direccion = models.CharField(maxlength=50,blank=True)
    telefonos = models.SlugField(blank=True)
    juez = models.ForeignKey(Juez)

    def __unicode__(self):
   	    return instancia + ' ' + tipo_fuero + ' ' + numero + ' de ' + ciudad

    class Admin:
        pass

   

class Causa(models.Model):
	caso = models.CharField(maxlength=100)
   	caratula = models.CharField(maxlength=100,blank=True)
   	joven = models.ManyToManyField(Joven,blank=True)
   	etapaJudicial = models.OneToOneField(EtapaJudicial)
   	fiscal = models.ForeignKey(Fiscal)
   	imputados = models.ForeignKey(Imputado)
   	punteo = models.TextField("Resumen de la causa", help_text="Puede usar codigo HTML para formatear y linkear su texto")
   	
   	
   	#observaciones = models.TextField(blank=True)
   	def __unicode__(self):
   	    return self.caso   	    

	class Admin:
		pass

class Incidente(models.Model):    
    caso_padre = models.OneToOneField(Causa)
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
	fecha_vencimiento = models.OneToOneField(Evento, blank=True)
	foja = models.CharField(maxlength=20)
	comentario = models.TextField()

	def lala(self):
		pass

	class Admin:
		pass



class SeguimientoIncidente(models.Model):
	fecha_ingreso = models.DateTimeField(auto_now_add=True)
	creado_por = models.ForeignKey(User)
	Incidente = models.ForeignKey(Incidente)
	#autor = models.ForeignKey(Usuario)
	fecha_vencimiento = models.OneToOneField(Evento, blank=True)
	foja = models.CharField(maxlength=20)
	comentario = models.TextField()

   	def __unicode__(self):
   	    return "seguimiento " + str(self.fecha_ingreso)

	class Admin:
		pass



