import json

from django.http import HttpResponse
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
