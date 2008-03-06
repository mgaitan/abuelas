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
		
FormPunteo = forms.form_for_model(ParrafoPunteo, fields=('texto'))

def seguimiento_form(request, causa_id):
    form_seguimiento = FormSeguimiento(request.POST)
    causa = Caso.objects.get(pk=causa_id)
    
    if request.method == 'POST':
        #procesado de Formularios.                
        if  form_seguimiento.is_valid():
            instance = form_seguimiento.save(commit=False)
            #agrego los campos que se cargan automaticamente
            instance.creado_por = request.user 
            instance.causa = causa
            
            instance.save()
            form_seguimiento = FormSeguimiento() #genero un formulario limpio
            return render_to_response('form_seguimiento.html',{'form_seguimiento': form_seguimiento, 'ok': True})
    else:
        form_seguimiento = FormSeguimiento()
        
    return render_to_response('form_seguimiento.html',{'form_seguimiento': form_seguimiento})
            
def redir(request, causa_id):
    return render_to_response('redir.html',{'causa_id': causa_id})    
    


def causa_detalle(request, causa_id):
    #que solapa aparece por defecto?
    if  request.GET.has_key('tab') :
        tab = request.GET['tab']
    else:
        tab = 0

    causa = Caso.objects.get(pk=causa_id)
    listas = {}
    listas["querellantes"] = causa.querellante.all()
    listas["imputados"] = causa.imputados.all()
    listas["jovenes"] = causa.joven.all()
    
    seguimientos = Seguimiento.objects.filter(Q(causa=causa_id)).order_by('-fecha_ingreso')
    punteos = ParrafoPunteo.objects.filter(Q(caso=causa_id)).order_by('-fecha_ingreso')
    
    if request.method == 'POST':
        #procesado de Formularios.       
        if request.POST["tipo"] == "punteo":
            #procesado del formulario de punteosss.
            
            form_punteo = FormPunteo(request.POST)            
            
            if  form_punteo.is_valid():            
                instance = form_punteo.save(commit=False)
                #agrego los campos que se cargan automaticamente
                instance.creado_por = request.user 
                instance.caso = causa               
                instance.save()
                #return HttpResponseRedirect('/causas/' + causa_id)

                return HttpResponseRedirect('/causas/' + causa_id + '/?tab=1')

            else:
                form_seguimiento = FormSeguimiento()                
                

    else:
        form_seguimiento = FormSeguimiento()
        form_punteo = FormPunteo()
    
    return render_to_response('detalle_causa.html', {'causa': causa,
        'listas': listas, 'seguimientos': seguimientos,
         'usuario': request.user.id, 'punteos': punteos, 'tab': tab })
	


def tabla_ajax(request, causa_id):
    causa = Caso.objects.get(pk=causa_id)
    sentido = {'asc': '', 'desc': '-'}
    columna = ['creado_por', 'fecha_ingreso', 'categoria', 'foja', 'comentario']
    
    seguimientos = Seguimiento.objects.filter(Q(causa=causa_id)).order_by(sentido[request.GET['dir']]+columna[int(request.GET['sort'])] )
    return render_to_response('tabla-ajax.html', {'seguimientos': seguimientos})
    


	

def juzgados(request):
    pagina = {}
    pagina["juzgados"] = Juzgado.objects.all().order_by('nombre_juzgado')
    pagina["titulo"] = "Juzgados"
    return render_to_response('juzgados.html', pagina)


def juzgados_detalle(request, juzgado_id):
    return HttpResponse("You're looking el juzgado %s." % juzgado_id)
    
    
