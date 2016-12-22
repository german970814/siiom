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
    """Vista para realizar busquedas de mienbros desde AJAX a los miembros que son lideres, y no lideran grupo."""

    red = Red.objects.get(pk=pk)

    if request.method == 'POST':

        form = BusquedaForm(data=request.POST)

        if form.is_valid():
            value = form.cleaned_data.get('value')
            grupo = form.cleaned_data.get('grupo', None)

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
                query_lideres = Grupo.objects.raiz().miembro_set.lideres_disponibles()

            if grupo is not None:
                query_lideres |= grupo.lideres.all()

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
