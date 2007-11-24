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
		
	
def causa_detalle(request, causa_id):
    causa = Caso.objects.get(pk=causa_id)

    listas = {}
    listas["querellantes"] = causa.querellante.all()
    listas["imputados"] = causa.imputados.all()
    listas["jovenes"] = causa.joven.all()
    
    seguimientos = Seguimiento.objects.filter(Q(causa=causa_id)).order_by('-fecha_ingreso')
    
    if request.method == 'POST':
        form = FormSeguimiento(request.POST)
        
        #agrego los campos que se cargan automaticamente

        if form.is_valid():
            instance = form.save(commit=False)
            instance.creado_por = request.user #aqui deberia conocer cual es el usuario logueado. 
            instance.causa = causa
            instance.save()
            return HttpResponseRedirect('/causas/' + causa_id)
    else:
        form = FormSeguimiento()
        
    return render_to_response('detalle_causa.html', {'causa': causa, 'listas': listas, 'seguimientos': seguimientos, 'form': form, 'usuario': request.user.id })
	
	

def juzgados(request):
    pagina = {}
    pagina["juzgados"] = Juzgado.objects.all().order_by('nombre_juzgado')
    pagina["titulo"] = "Juzgados"
    return render_to_response('juzgados.html', pagina)


def juzgados_detalle(request, juzgado_id):
	 return HttpResponse("You're looking el juzgado %s." % juzgado_id)
    
    
