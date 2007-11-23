from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django import newforms as forms
from django.db.models import Q
from abuelas.seguimiento.models import *

#formularios

FormSeguimiento = forms.form_for_model(Seguimiento)

# Create your views here.

def causas(request):
    pagina = {}
    pagina["causas"] = Caso.objects.all().order_by('nombre_caso')
    pagina["titulo"] = "Listado de Causas"
    return render_to_response('causas.html', pagina)    
		
	
def causa_detalle(request, causa_id):
    causa = Caso.objects.get(pk=causa_id)

    listas = {}
    listas["querellantes"] = causa.querellante.all()
    listas["imputados"] = causa.imputados.all()
    listas["jovenes"] = causa.joven.all()
    
    seguimientos = Seguimiento.objects.filter(Q(causa=causa_id)).order_by('-fecha_ingreso')
    
    if request.method == 'POST':
        form = FormSeguimiento(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.save()
            
            return HttpResponseRedirect('/causas/' + causa_id)
    else:
        form = FormSeguimiento()
        
    return render_to_response('detalle_causa.html', {'causa': causa, 'listas': listas, 'seguimientos': seguimientos, 'form': form})
	
	

def juzgados(request):
    pagina = {}
    pagina["juzgados"] = Juzgado.objects.all().order_by('nombre_juzgado')
    pagina["titulo"] = "Juzgados"
    return render_to_response('juzgados.html', pagina)


def juzgados_detalle(request, juzgado_id):
	 return HttpResponse("You're looking el juzgado %s." % juzgado_id)
    
    
