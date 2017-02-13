import json

from django.http import HttpResponse
from django.core import serializers
from common.decorators import login_required_api
from .models import Grupo


@login_required_api
def lideres_grupo(request, pk):
    """
    Permite a un usuario logueado ver los lideres del grupo.
    """

    grupo = Grupo.objects.iglesia(request.iglesia).get(pk=pk)
    response = [{'pk': lider.pk, 'nombre': str(lider)} for lider in grupo.lideres.all()]
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required_api
def discipulos_miembros_grupo(request, pk):
    """
    Retorna un JSON con los discipulos y miembros de un grupo.
    """

    grupo = Grupo.objects.iglesia(request.iglesia).get(pk=pk)
    string = serializers.serialize(
        queryset=grupo.miembros.all().order_by('nombre'),
        format='json', fields=['nombre', 'primerApellido']
    )
    serialized = json.loads(string)
    return HttpResponse(json.dumps(serialized), content_type='application/json')
