from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.db.models import Q

from .forms import FormularioObtenerGrupoAPI
from grupos.models import Red, Grupo
from common.constants import RESPONSE_SUCCESS, RESPONSE_CODE, RESPONSE_ERROR, RESPONSE_DENIED, URL_SIN_PERMISOS as URL
from common.groups_tests import tesorero_administrador_test

import json


@user_passes_test(tesorero_administrador_test, login_url=URL)
def obtener_grupos(request):
    """Vista que devuelve una lista de grupos en JSON de acuerdo a un valor inicial enviado."""

    if request.method == 'POST':
        form = FormularioObtenerGrupoAPI(data=request.POST)

        if form.is_valid():
            red = form.cleaned_data.get('red')
            value = form.cleaned_data.get('value')

            querys = (
                Q(lideres__nombre__icontains=value) |
                Q(lideres__primerApellido__icontains=value) |
                Q(lideres__cedula__icontains=value)
            )

            grupos = Grupo.objects.filter(
                querys, red=red
            ).prefetch_related('lideres').distinct()[:10]

            response = {
                'grupos': [{'id': str(x.id), 'nombre': str(x)} for x in grupos],
                RESPONSE_CODE: RESPONSE_SUCCESS
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
