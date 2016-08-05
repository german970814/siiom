# Django Package
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Locale Apps
from .models import Requisicion

# Python Package
import json


@login_required
@csrf_exempt
def detalles_requisicion_api(request, id_requisicion):
    """
    Devuelve en formato json los detalles de una requisicion
    """

    try:
        requisicion = Requisicion.objects.get(id=id_requisicion)

        data = [
            {
                'cantidad': detalle.cantidad or 1, 'descripcion': detalle.descripcion,
                'referencia': detalle.referencia or '', 'marca': detalle.marca or '',
                'valor_aprobado': detalle.valor_aprobado or 0, 'total_aprobado': detalle.total_aprobado or 0,
                'forma_pago': detalle.get_forma_pago_display()
            } for detalle in requisicion.detallerequisicion_set.all()
        ]

        return HttpResponse(json.dumps(data), content_type='application/json')
    except:
        return HttpResponse('', content_type='text/plain')


@login_required
@csrf_exempt
def observaciones_requisicion(request, id_requisicion):
    """
    Devuelve la observacion ligada a la requisicion y el nombre del usuario
    """

    try:
        requisicion = Requisicion.objects.get(id=id_requisicion)
        data = []
        data1 = [
            {
                'observacion': historia.observacion,
                'usuario': historia.empleado.__str__()
            } for historia in requisicion.historial_set.all() if historia.observacion
        ]
        data2 = [
            {
                'archivo': archivo.archivo.url,
                'ruta': archivo.archivo.url
            } for archivo in requisicion.adjunto_set.all()
        ]
        data.insert(0, data1)
        if data2:
            data.insert(1, data2)
        return HttpResponse(json.dumps(data), content_type='application/json')
    except:
        return HttpResponse('', content_type='text/plain')


@login_required
@csrf_exempt
def requisicion_comentada_api(request, id_requisicion):
    """
    Retorna un valor para ser evaluado en javascript con true o false si esta comentada
    devuelve true si fue comentada por jefe de departamento
    """
    # if requisicion.historial_set.last().empleado.usuario.has_perm('organizacional.es_compras'):
    try:
        requisicion = Requisicion.objects.get(id=id_requisicion)
        _choices = [Requisicion.DATA_SET['administrativo'], Requisicion.DATA_SET['compras']]
        if requisicion.get_rastreo() in _choices:
            return HttpResponse('true', content_type='text/plain')
        else:
            return HttpResponse('false', content_type='text/plain')
    except:
        return HttpResponse('', content_type='text/plain')


@login_required
@csrf_exempt
def requisicion_comentada_compras_api(request, id_requisicion):
    """
    Retorna un valor para ser evaluado en javascript con true o false si esta comentada
    devuelve true si fue comentada por usuario de compras
    """
    # if requisicion.historial_set.last().empleado.usuario.has_perm('organizacional.es_compras'):
    try:
        requisicion = Requisicion.objects.get(id=id_requisicion)
        _choices = [Requisicion.DATA_SET['administrativo']]
        if requisicion.get_rastreo() in _choices:
            return HttpResponse('true', content_type='text/plain')
        else:
            return HttpResponse('false', content_type='text/plain')
    except:
        return HttpResponse('', content_type='text/plain')


@login_required
@csrf_exempt
def requisicion_comentada_jefe_administrativo_api(request, id_requisicion):
    """
    Retorna un valor para ser evaluado en javascript con true o false si esta comentada
    devuelve true si fue comentada por jefe administrativo
    """

    try:
        requisicion = Requisicion.objects.get(id=id_requisicion)
        _choices = [Requisicion.DATA_SET['financiero']]
        if requisicion.get_rastreo() in _choices:
            return HttpResponse('true', content_type='text/plain')
        else:
            return HttpResponse('false', content_type='text/plain')
    except:
        return HttpResponse('', content_type='text/plain')
