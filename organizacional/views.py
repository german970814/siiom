# Django Package
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Locale Apps
# from gestion_documental.models import Documento
from .models import Area, Departamento

# Python Package
import json


@csrf_exempt
def areas_departamento_json(request):
    """
    Vista que devuelve una lista de areas a partir de un departamento en formato json
    """

    if request.method == 'POST':
        departamento = get_object_or_404(Departamento, pk=request.POST['id_departamento'])

        areas = Area.objects.filter(departamento__id=departamento.id)

        response = [{'id': area.id, 'area': area.nombre} for area in areas]

        return HttpResponse(json.dumps(response), content_type='application/json')
