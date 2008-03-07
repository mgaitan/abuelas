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
FormMarcas = forms.form_for_model(MarcasPunteo, fields=('categoria', 'comentario', 'importante', 'fecha_incidente', 'imputados', 'testigos'))

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
            

def punteo_form(request, causa_id):
    form_punteo = FormPunteo(request.POST)
    causa = Caso.objects.get(pk=causa_id)
    if request.method == 'POST':
        #procesado de Formularios.                
        if  form_punteo.is_valid():
            instance = form_punteo.save(commit=False)
            #agrego los campos que se cargan automaticamente
            instance.creado_por = request.user 
            instance.caso = causa
            instance.save()
            form_punteo = FormPunteo() #genero un formulario limpio
            return render_to_response('form_punteo.html',{'form_punteo': form_punteo, 'ok': True})
    else:
        form_punteo = FormPunteo()       
    return render_to_response('form_punteo.html',{'form_punteo': form_punteo})

def marcas_form(request, causa_id, parrafo_id):
    form_marca = FormMarcas(request.POST)
    parrafo = ParrafoPunteo.objects.get(pk=parrafo_id)
    causa = Caso.objects.get(pk=causa_id)
    marcas = MarcasPunteo.objects.filter(Q(causa=causa_id) & Q(parrafo=parrafo_id)).order_by('-fecha_ingreso')
    ok = False
    if request.method == 'POST':
        if form_marca.is_valid(): 
            instance = form_marca.save(commit=False)  
            #agrego los campos que se cargan automaticamente
            instance.creado_por = request.user 
            instance.causa = causa            
            instance.parrafo = parrafo
            instance.save()
            form_marca = FormMarcas() #formulario limpio
            ok = True
            return render_to_response('form_marcas.html',{'form_marca': form_marca,
    'marcas': marcas, 'ok': ok, 'causa_id': causa.id, 'parrafo':parrafo})    
    else:
        form_marca = FormMarcas() #formulario limpio
    return render_to_response('form_marcas.html',{'form_marca': form_marca,
    'marcas': marcas, 'ok': ok, 'causa_id': causa.id, 'parrafo':parrafo})


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
    punteos = [(parrafin, len(MarcasPunteo.objects.filter(Q(parrafo=parrafin)))) for parrafin in punteos]
    
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
    
    
