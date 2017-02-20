# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from django.utils.module_loading import import_string
from django.shortcuts import get_object_or_404

from .forms import BusquedaForm
from .constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_CODE, RESPONSE_DENIED
from .decorators import login_required_api
from miembros.models import Miembro
from grupos.models import Grupo

import json


Red = import_string('grupos.models.Red')


@login_required_api
def busqueda_miembro_api(request, pk):
    """
    Vista obtener los miembros lideres de una red especifica.

    :returns:
        Un diccionario de 10 Miembros(max.) lideres que se encuentren disponibles a partir de la red.

    :rtype: dict

    :param pk:
        El pk de la red a partir de la cual se buscarán los líderes.

    La vista inicialmente recibe datos en el método POST, y espera recibir los parametros de:

        * ``value*``: Será el valor parametro de búsqueda de lideres.

        * ``grupo (opcional)``: Se agregarán al queryset los lideres de este grupo.

        * ``grupo_by (opcional)``: Grupo a partir del cual se consultaran, solo se mostrarán
          lideres que esten en el organigrama de este grupo.
    """

    red = Red.objects.iglesia(request.iglesia).get(pk=pk)

    if request.method == 'POST':

        form = BusquedaForm(data=request.POST)

        if form.is_valid():
            value = form.cleaned_data.get('value')
            grupo = form.cleaned_data.get('grupo', None)
            grupo_by = form.cleaned_data.get('grupo_by', None)

            querys = (
                Q(nombre__icontains=value) |
                Q(primerApellido__icontains=value) |
                Q(segundoApellido__icontains=value) |
                Q(cedula__icontains=value)
            )

            query_lideres = Miembro.objects.lideres_disponibles().red(red).only(
                'nombre', 'cedula', 'primerApellido', 'segundoApellido'
            )

            if not query_lideres.exists():
                query_lideres = Grupo.objects.raiz(request.iglesia).miembros.lideres_disponibles()

            if grupo is not None:
                query_lideres |= grupo.lideres.all()

            if grupo_by is not None:
                querys |= Q(grupo__in=grupo_by.grupos_red.values_list('id', flat=1))

            miembros = query_lideres.filter(querys).distinct()[:10]

            response = {
                'miembros': [{'id': str(x.id), 'nombre': str(x)} for x in miembros],
                RESPONSE_CODE: RESPONSE_SUCCESS,
                'value': value
            }

        else:
            _errors = []
            for error in form.errors:
                _errors.append(error)
            response = {
                'error': ', '.join(_errors),
                RESPONSE_CODE: RESPONSE_ERROR
            }
    else:
        response = {
            RESPONSE_CODE: RESPONSE_DENIED
        }

    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required_api
def busqueda_grupo_api(request, pk):
    """
    Vista para realizar las busquedas a grupos por caracteres, de acuerdo a una red.

    :param pk:
        Es el pk de un grupo, dicho grupo nos dará la red a partir de la cual se efectuará la busqueda

    :returns:
        Un JSON que contiene los grupos filtrados por Nombre de lideres, Primer Apellido de lideres,
        Cedula de lideres o el nombre del grupo.

    .. note::

        Se debe enviar por GET una variable llamada 'value', a partir de la cual iniciaría la busqueda.
    """

    grupo = get_object_or_404(Grupo, pk=pk, iglesia=request.iglesia)

    if request.method == 'GET' and request.is_ajax():
        form = BusquedaForm(data=request.GET)

        if form.is_valid():
            q = form.cleaned_data.get('value')
            querys = (
                Q(lideres__nombre__icontains=q) |
                Q(lideres__primerApellido__icontains=q) |
                Q(nombre__icontains=q) |
                Q(lideres__cedula__icontains=q)
            )

            queryset = Grupo.objects.red(grupo.red).filter(querys).distinct()[:10]

            response = {
                'grupos': [{'id': grupo.pk, 'nombre': grupo.__str__()} for grupo in queryset.iterator()],
                RESPONSE_CODE: RESPONSE_SUCCESS,
                'value': q
            }

            return HttpResponse(json.dumps(response), content_type='application/json')

    return HttpResponseBadRequest('Bad Request')
