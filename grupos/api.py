# Django imports
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Locale imports
from common.decorators import login_required_api
from common import constants
from .models import Grupo

# Python imports
import json


@login_required_api
def lideres_grupo(request, pk):
    """
    :returns:
        Un JSON con los lideres del grupo pasado en el pk.

    :param pk:
        El pk de el grupo a partir del cual se quieren sacar los lideres.
    """

    grupo = Grupo.objects.get(pk=pk)
    response = [{'pk': lider.pk, 'nombre': str(lider)} for lider in grupo.lideres.all()]
    return HttpResponse(json.dumps(response), content_type=constants.CONTENT_TYPE_API)


@login_required_api
def discipulos_miembros_grupo(request, pk):
    """
    :returns:
        Un JSON con los discipulos y miembros de un grupo.

    :param pk:
        El pk de el grupo a partir del cual se quieren obtener los miembros y discipulos.
    """

    grupo = get_object_or_404(Grupo, pk=pk)

    string = serializers.serialize(
        queryset=grupo.miembros.all().order_by('nombre'),
        format='json', fields=['nombre', 'primer_apellido']
    )

    serialized = json.loads(string)
    return HttpResponse(json.dumps(serialized), content_type=constants.CONTENT_TYPE_API)
