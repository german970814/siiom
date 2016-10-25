from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages
from django.utils.translation import ugettext as _

from common.forms import FormularioRangoFechas
from common.tests import adminTest
from miembros.models import Miembro
from grupos.models import Grupo, Red
from .utils import clean_direccion


@user_passes_test(adminTest)
def asignar_grupo_visitas(request):
    """
    Vista para asignar a las visitas a un grupo
    """

    data = {}

    if request.method == 'POST':
        form = FormularioRangoFechas(data=request.POST)

        if form.is_valid():
            fecha_inicial = form.cleaned_data['fecha_inicial']
            fecha_final = form.cleaned_data['fecha_final']

            visistas = Miembro.objects.visitas(
                fechaRegistro__range=(fecha_inicial, fecha_final)
            )

            grupos = Grupo.objects.filter(estado='A').select_related('lider1', 'lider2', 'red').values_list(
                'direccion', 'id', 'nombre', 'red__nombre'
            )

            grupos = [list(x) for x in grupos]

            data['visitas'] = visistas
            data['redes'] = Red.objects.all()
            if visistas.exists():
                data['grupos'] = grupos

            messages.success(request, _('Exito'))
        else:
            messages.error(request, _('Ha ocurrido un error'))
    else:
        form = FormularioRangoFechas()

    data['form'] = form

    return render(request, 'consolidacion/asignar_grupo_visitas.html', data)
