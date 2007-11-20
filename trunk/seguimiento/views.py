from django.http import HttpResponse
from django.shortcuts import render_to_response
from abuelas.seguimiento.models import Juzgado
# Create your views here.

def juzgados(request):
	juzgados = Juzgado.objects.all().order_by('nombre_juzgado')
	return render_to_response('juzgados.html', {'lista_juzgados': juzgados})


def juzgados_detalle(request, juzgado_id):
	 return HttpResponse("You're looking el juzgado %s." % juzgado_id)
    
    