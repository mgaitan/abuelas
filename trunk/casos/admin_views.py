#!/usr/bin/env python
#coding=utf-8
from abuelas.casos.models import *
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.main import change_stage

def reporte_caso(request, caso_id):
    caso = get_object_or_404(Caso, pk=caso_id)
    
    listas = {}
    listas["querellantes"] = caso.querellante.all()
    listas["imputados"] = caso.imputados.all()
    listas["jovenes"] = caso.joven.all()
   
    
    if not request.GET.has_key('edit'):
        return render_to_response(
            "admin/casos/reporte_caso.html",
            {'caso': caso,'listas': listas },
            RequestContext(request, {}),
        )
    else:
        #vista de edicion!
        return change_stage(request, 'casos', 'caso', caso_id)
    
