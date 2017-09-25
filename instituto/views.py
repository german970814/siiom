from django.forms import inlineformset_factory
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Case, Value, F, Count, When, CharField

from waffle.decorators import waffle_switch

from . import models, resources
from miembros.models import Miembro
from .forms import (
    FormularioMateria, FormularioModulo, FormularioSesion, ReporteInstitutoForm
)

__author__ = 'German Alzate'


def crear_materia(request):
    """
    Vista de creación de una materia, también sirve para crear modulos y sesiones.
    """

    data = {}

    ModuloFormSet = inlineformset_factory(
        models.Materia, models.Modulo, fk_name='materia',
        form=FormularioModulo, min_num=1, extra=1,
        validate_min=True, can_delete=False
    )

    if request.method == 'POST':
        formulario_materia = FormularioMateria(request.POST)
        if formulario_materia.is_valid():
            materia = formulario_materia.save(commit=False)
            formulario_modulo 
            materia.save()
    else:
        formulario_materia = FormularioMateria()

    data['formulario_materia'] = formulario_materia

    return render(request, 'istituto/crear_materia.html', data)


def lista_estudiantes_sesion(request):
    from django.shortcuts import render
    return render(request, 'academia/lista_estudiantes_sesion.html', {})


@waffle_switch('instituto')
@permission_required('miembros.es_administrador', raise_exception=True)
def reporte_instituto(request):

    if request.method == 'POST':
        form = ReporteInstitutoForm(data=request.POST)
        if form.is_valid():
            grupo = form.cleaned_data.get('grupo')
            materias = form.cleaned_data.get('materias', models.Materia.objects.all())

            grupos = grupo._grupos_red.prefetch_related('lideres')
            lideres = Miembro.objects.filter(id__in=grupos.values_list('lideres__id', flat=True))

            if not materias.exists():
                materias = models.Materia.objects.all()

            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=reporte.xlsx'
            excel = resources.ReporteInstituto(data=lideres, materias=materias)
            response.write(excel.read())
            return response

    else:
        form = ReporteInstitutoForm()
    return render(request, 'instituto/reporte_instituto.html', {'form': form})