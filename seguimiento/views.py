from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django import newforms as forms
from django.db.models import Q
from abuelas.seguimiento.models import *
from django.contrib.auth.models import User


# Create your views here.

def causas(request):
    pagina = {}
    pagina["causas"] = Caso.objects.all().order_by('nombre_caso')
    pagina["titulo"] = "Listado de Causas"
    return render_to_response('causas.html', pagina)    

#formularios
FormSeguimiento = forms.form_for_model(Seguimiento, fields=('categoria', 'foja','importante', 'comentario'))
		
class FormPunteo(forms.Form):
    punteo = forms.CharField(widget=forms.Textarea, label="")

		
	
def causa_detalle(request, causa_id):
    causa = Caso.objects.get(pk=causa_id)

    listas = {}
    listas["querellantes"] = causa.querellante.all()
    listas["imputados"] = causa.imputados.all()
    listas["jovenes"] = causa.joven.all()
    
    seguimientos = Seguimiento.objects.filter(Q(causa=causa_id)).order_by('-fecha_ingreso')
    
    if request.method == 'POST':
        #procesado de Formularios.
               
        
        if request.POST["tipo"] == "punteo":
            #procesado del formulario de punteosss.
            
            form_punteo = FormPunteo(request.POST)            
            
            if  form_punteo.is_valid():            
                causa.punteo = request.POST["punteo"]
                causa.save()
                return HttpResponseRedirect('/causas/' + causa_id)
            else:
                form_seguimiento = FormSeguimiento()                
                
        elif request.POST["tipo"] == "seguimiento":
            #procesaso del formulario de seguimiento

            form_seguimiento = FormSeguimiento(request.POST)
            
            if  form_seguimiento.is_valid():
                instance = form_seguimiento.save(commit=False)

                #agrego los campos que se cargan automaticamente
                instance.creado_por = request.user 
                instance.causa = causa
                
                instance.save()
                return HttpResponseRedirect('/causas/' + causa_id)
            else:
                form_punteo = FormPunteo()
                
    else:
        form_seguimiento = FormSeguimiento()
        form_punteo = FormPunteo()
    
    return render_to_response('detalle_causa.html', {'causa': causa, 'listas': listas, 'seguimientos': seguimientos, 'form_seguimiento': form_seguimiento, 'form_punteo': form_punteo, 'usuario': request.user.id })
	
	

def juzgados(request):
    pagina = {}
    pagina["juzgados"] = Juzgado.objects.all().order_by('nombre_juzgado')
    pagina["titulo"] = "Juzgados"
    return render_to_response('juzgados.html', pagina)


def juzgados_detalle(request, juzgado_id):
	 return HttpResponse("You're looking el juzgado %s." % juzgado_id)
    
    
