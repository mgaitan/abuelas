#!/usr/bin/env python
#coding=utf-8
from abuelas.documentos.models import Documento
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required


def listado(request):
    return render_to_response(
        "admin/documentos/listado.html",
        {'doc_listado' : Documento.objects.all()},
        RequestContext(request, {}),
    )
listado = staff_member_required(listado)
