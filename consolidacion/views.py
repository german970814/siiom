from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.conf import settings

from .utils import clean_direccion
from .models import Visita
from .forms import FormularioVisita, FormularioAsignarGrupoVisita
from common.forms import FormularioRangoFechas
from common.groups_tests import adminTest
from miembros.models import Miembro
from grupos.models import Grupo, Red

import json


class VisitasCBVMixxing(object):
    """
    Base de clases para visitas
    """
    model = Visita

    def form_invalid(self, form):
        messages.error(self.request, _("Ha ocurrido un error al enviar el formulario"))
        return super(VisitasCBVMixxing, self).form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, _("Visita guardada con exito"))
        return super(VisitasCBVMixxing, self).form_valid(form)


class CrearVisita(VisitasCBVMixxing, CreateView):
    """
    CBV para crear visitas
    """
    form_class = FormularioVisita
    template_name = 'consolidacion/crear_visita.html'
    success_url = reverse_lazy('consolidacion:crear_visita')


class EditarVisita(VisitasCBVMixxing, UpdateView):
    """
    CBV para editar Visitas
    """
    form_class = FormularioVisita
    template_name = 'consolidacion/crear_visita.html'

    def form_valid(self, form):
        self.success_url = reverse_lazy('consolidacion:editar_visita', args=(form.instance.id,))
        return super(EditarVisita, self).form_valid(form)


def asignar_grupo_visitas_ajax(request):
    """
    Vista para asignar los grupos desde una llamada ajax
    """

    data = {}
    if request.method == 'POST':
        form = FormularioAsignarGrupoVisita(data=request.POST)

        if form.is_valid():
            grupo = form.cleaned_data.get('grupo')
            visita = form.cleaned_data.get('visita')

            visita.grupo = grupo
            visita.save()
            data = {
                'response_code': 200,
                'message': 'Visita Asignada a grupo (%s) exitosamente' % grupo.get_nombre(),
                'id_visita': visita.id
            }
        else:
            if settings.DEBUG:
                print(form.errors)
            data = {
                'response_code': 401,
                'message': 'Ocurrieron errores al enviar el formulario'
            }
    else:
        data = {
            'response_code': 405,
            'message': 'INVALID REQUEST'
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(adminTest)
def asignar_grupo_visitas(request):
    """
    Vista para asignar a las visitas a un grupo
    """

    data = {}

    if request.method == 'POST':
        # print(request.POST)
        if 'visita[]' in request.POST:
            response = {}
            _removed_ids = []
            try:
                # print(request.POST)
                visitas = request.POST.getlist('visita[]')
                for visita in visitas:
                    try:
                        _visita = Visita.objects.get(id=visita)
                        _visita.retirado = True
                        _visita.save()
                        _removed_ids.append(_visita.id)
                    except Exception as exception:
                        # if settings.DEBUG:
                            # print(exception)
                        response['error'] = exception.__str__()
                        response['response_code'] = 401
                if 'error' not in response:
                    response['message'] = 'SUCCESS'
                    response['response_code'] = 200
                    response['removed_ids'] = _removed_ids
            except Exception as exception:
                if settings.DEBUG:
                    print(exception)
                response['error'] = exception.__str__()
                response['response_code'] = 502

            return HttpResponse(json.dumps(response), content_type='application/json')

        else:
            form = FormularioRangoFechas(data=request.POST)

            if form.is_valid():
                fecha_inicial = form.cleaned_data['fecha_inicial']
                fecha_final = form.cleaned_data['fecha_final']

                # visitas = Miembro.objects.visitas(
                #     fechaRegistro__range=(fecha_inicial, fecha_final)
                # )

                visitas = Visita.objects.filter(
                    fecha_ingreso__range=(fecha_inicial, fecha_final),
                    retirado=False
                ).exclude(grupo__isnull=False)

                grupos = Grupo.objects.prefetch_related('lideres').filter(estado='A').select_related('red')

                if visitas.exists():
                    data['visitas'] = visitas
                    data['redes'] = Red.objects.all()
                    data['grupos'] = grupos
                    messages.success(request, _('Se muestran %d visitas para el rango de fechas escogido' % visitas.count()))
                else:
                    messages.warning(request, _('No se encontraron resultados para el rango de fecha escogido'))
            else:
                messages.error(request, _('Ha ocurrido un error al enviar el formulario'))
    else:
        form = FormularioRangoFechas()

    data['form'] = form

    return render(request, 'consolidacion/asignar_grupo_visitas.html', data)
