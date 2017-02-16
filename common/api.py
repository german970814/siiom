# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.utils.module_loading import import_string

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
        Un array de 10 Miembros(max.) lideres que se encuentren disponibles a partir de la red.

    :rtype: list

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
