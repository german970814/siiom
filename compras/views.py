# Django Packages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.db import transaction
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required

# Third Apps
from waffle.decorators import waffle_switch

# Locale Apps
from .forms import (
    FormularioSolicitudRequisicion, FormularioDetalleRequisicion, FormularioAdjunto,
    FormularioRequisicionesJefe, FormularioRequisicionesCompras, FormularioObservacionHistorial
)
from .models import DetalleRequisicion, Requisicion, Adjunto, Historial


@waffle_switch('compras')
@login_required
@transaction.atomic
def crear_requisicion(request):
    """
    Vista para la creacion de requisiciones en el modulo de compras
    """
    try:
        empleado = request.user.empleado
    except:
        raise Http404

    DetalleRequisicionFormSet = inlineformset_factory(
        Requisicion, DetalleRequisicion, fk_name='requisicion',
        form=FormularioDetalleRequisicion, min_num=1, extra=4,
        validate_min=True, can_delete=False
    )

    AdjuntoFormset = inlineformset_factory(
        Requisicion, Adjunto, fk_name='requisicion',
        form=FormularioAdjunto, min_num=0, extra=1,
        validate_min=True, can_delete=False
    )

    if request.method == 'POST':
        form = FormularioSolicitudRequisicion(data=request.POST)
        formset_detalles = DetalleRequisicionFormSet(data=request.POST)
        formset_adjunto = AdjuntoFormset(request.POST, request.FILES)
        if form.is_valid():
            requisicion = form.save(commit=False)
            requisicion.empleado = empleado
            formset_detalles = DetalleRequisicionFormSet(data=request.POST, instance=requisicion)
            formset_adjunto = AdjuntoFormset(request.POST, request.FILES, instance=requisicion)
            if formset_detalles.is_valid() and formset_adjunto.is_valid():
                requisicion.save()
                formset_adjunto.save()
                formset_detalles.save()
                messages.success(request, _("Se ha creado la requisicion con éxito"))
                return redirect('compras:crear_requisicion')
            else:
                messages.error(request, _("Ha ocurrido un error al enviar el formulario"))
        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))

    else:
        form = FormularioSolicitudRequisicion()
        formset_detalles = DetalleRequisicionFormSet()
        formset_adjunto = AdjuntoFormset()

    data = {'form': form, 'formset_detalles': formset_detalles, 'formset_adjunto': formset_adjunto}

    return render(request, 'compras/crear_requisicion.html', data)


@waffle_switch('compras')
@login_required
@transaction.atomic
def editar_requisicion(request, id_requisicion):
    """
    Vista para la edicion de requisiciones, siempre y cuando esta se encuentre en estado PENDIENTE
    """
    try:
        requisicion = Requisicion.objects.get(id=id_requisicion)
        if requisicion.estado != Requisicion.PENDIENTE:
            raise Http404
    except Requisicion.DoesNotExist:
        raise Http404
    empleado = requisicion.empleado
    if empleado != request.user.empleado:
        return redirect('sin_permiso')

    DetalleRequisicionFormSet = modelformset_factory(
        DetalleRequisicion, form=FormularioDetalleRequisicion,
        min_num=1, extra=0, validate_min=True, can_delete=True
    )

    AdjuntoFormset = modelformset_factory(
        Adjunto, form=FormularioAdjunto, min_num=0, extra=1,
        validate_min=False, can_delete=True
    )

    if request.method == 'POST':
        form = FormularioSolicitudRequisicion(data=request.POST, instance=requisicion)
        formset_detalles = DetalleRequisicionFormSet(
            prefix='detallerequisicion_set',
            queryset=requisicion.detallerequisicion_set.all()
        )
        formset_adjunto = AdjuntoFormset(
            prefix='adjunto_set',
            queryset=requisicion.adjunto_set.all()
        )
        if form.is_valid():
            formset_detalles = DetalleRequisicionFormSet(
                data=request.POST, prefix='detallerequisicion_set',
                queryset=requisicion.detallerequisicion_set.all()
            )
            formset_adjunto = AdjuntoFormset(
                data=request.POST, files=request.FILES, prefix='adjunto_set',
                queryset=requisicion.adjunto_set.all()
            )
            if formset_adjunto.is_valid() and formset_detalles.is_valid():
                requisicion = form.save()
                for form_adjunto in formset_adjunto:
                    if form_adjunto.cleaned_data.get('DELETE', False) and hasattr(form_adjunto.instance, 'pk'):
                        if form_adjunto.instance.id is not None or form_adjunto.instance.pk is not None:
                            form_adjunto.instance.delete()
                        continue
                    form_adjunto.instance.requisicion = requisicion
                    if not form_adjunto.cleaned_data.get('archivo', False):
                        continue
                    form_adjunto.save()

                for form_detalle in formset_detalles:
                    if form_detalle.cleaned_data.get('DELETE', False) and hasattr(form_detalle.instance, 'pk'):
                        if form_detalle.instance.id is not None or form_detalle.instance.pk is not None:
                            form_detalle.instance.delete()
                        continue
                    form_detalle.instance.requisicion = requisicion
                    if not form_detalle.cleaned_data.get('descripcion', False):
                        continue
                    form_detalle.save()
                # formset_detalles.save()
                # formset_adjunto.save()
                messages.success(request, _("Se ha editado la requisicion con éxito"))
                return redirect(reverse('compras:editar_requisicion', args=(id_requisicion, )))
            else:
                messages.error(request, _("Ha ocurrido un error al enviar el formulario"))
        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))

    else:
        form = FormularioSolicitudRequisicion(instance=requisicion)
        formset_detalles = DetalleRequisicionFormSet(
            prefix='detallerequisicion_set', queryset=requisicion.detallerequisicion_set.all()
        )
        formset_adjunto = AdjuntoFormset(
            prefix='adjunto_set', queryset=requisicion.adjunto_set.all()
        )

    data = {
        'requisicion': requisicion, 'formset_detalles': formset_detalles,
        'formset_adjunto': formset_adjunto, 'form': form
    }

    return render(request, 'compras/crear_requisicion.html', data)


@waffle_switch('compras')
@login_required
def ver_requisiciones_empleado(request):
    """
    Vista para la vista de las requisiciones hechas por el empleado del request
    """

    empleado = request.user.empleado

    requisiciones = empleado.requisicion_set.all().order_by(
        '-fecha_ingreso'
    ).prefetch_related('detallerequisicion_set')

    data = {'requisiciones': requisiciones}

    return render(request, 'compras/ver_requisiciones_empleado.html', data)


@waffle_switch('compras')
@login_required
def ver_requisiciones_jefe_departamento(request):
    """
    Vista para ver las requisiciones que se han hecho a un departamento
    """
    empleado = request.user.empleado
    if not empleado.jefe_departamento:
        return redirect('sin_permiso')

    requisiciones = Requisicion.objects.filter(
        empleado__areas__departamento__in=request.user.empleado.areas.departamentos()
    ).exclude(historial__estado=Historial.RECHAZADA).order_by('-fecha_ingreso')

    if request.method == 'POST':
        form = FormularioRequisicionesJefe(data=request.POST)
        if form.is_valid():
            requisicion = Requisicion.objects.get(id=form.cleaned_data['id_requisicion'])
            if 'aprobar' in request.POST:
                historial = requisicion.crear_historial(empleado=empleado, estado=Historial.APROBADA)
                mensaje = 'aprobado'
                requisicion.estado = Requisicion.PROCESO
                requisicion.save()
            elif 'rechazar' in request.POST:
                historial = requisicion.crear_historial(empleado=empleado, estado=Historial.RECHAZADA)
                mensaje = 'rechazado'
            historial.save()
            messages.success(
                request,
                _("Se ha {} la requisicion No.{} exitosamente").format(mensaje, requisicion.id)
            )
            return redirect('compras:ver_requisiciones_jefe_departamento')
        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))
    else:
        form = FormularioRequisicionesJefe()

    data = {'requisiciones': requisiciones, 'form': form}

    return render(request, 'compras/ver_requisiciones_jefe_departamento.html', data)


@waffle_switch('compras')
@permission_required('organizacional.es_compras')
def ver_requisiciones_compras(request):
    """
    Vista para ver las requisiciones que se han hecho desde un usuario de compras
    """
    empleado = request.user.empleado

    requisiciones = Requisicion.objects.aprobadas_jefe_departamento().order_by('-fecha_ingreso')

    if request.method == 'POST':
        form = FormularioRequisicionesCompras(data=request.POST)
        if form.is_valid():
            requisicion = Requisicion.objects.get(id=form.cleaned_data['id_requisicion'])
            if 'aprobar' in request.POST:
                if 'observacion' in form.cleaned_data:
                    historial = requisicion.crear_historial(
                        empleado=empleado, estado=Historial.APROBADA,
                        observacion=form.cleaned_data['observacion']
                    )
                else:
                    historial = requisicion.crear_historial(empleado=empleado, estado=Historial.APROBADA)
                mensaje = 'aprobado'
            elif 'rechazar' in request.POST:
                if 'observacion' in form.cleaned_data:
                    historial = requisicion.crear_historial(
                        empleado=empleado, estado=Historial.RECHAZADA,
                        observacion=form.cleaned_data['observacion']
                    )
                else:
                    historial = requisicion.crear_historial(empleado=empleado, estado=Historial.RECHAZADA)
                mensaje = 'rechazado'
            historial.save()
            messages.success(
                request,
                _("Se ha {} la requisición No.{} con exito".format(mensaje, requisicion.id))
            )
            return redirect('compras:ver_requisiciones_compras')
        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))
    else:
        form = FormularioRequisicionesCompras()

    data = {'requisiciones': requisiciones, 'form': form}

    return render(request, 'compras/ver_requisiciones_compras.html', data)


@waffle_switch('compras')
@permission_required('organizacional.es_compras')
def adjuntar_archivos_requisicion(request, id_requisicion):
    """
    Vista para adjuntar archivos a una requisicion
    """

    requisicion = get_object_or_404(Requisicion, pk=id_requisicion)

    AdjuntoFormset = modelformset_factory(
        Adjunto, form=FormularioAdjunto, min_num=0, extra=1,
        validate_min=False, can_delete=True
    )

    if request.method == 'POST':
        form_historial = FormularioObservacionHistorial(data=request.POST, instance=requisicion.historial_set.last())
        formset_adjunto = AdjuntoFormset(data=request.POST, files=request.FILES, queryset=requisicion.adjunto_set.all())

        if formset_adjunto.is_valid() and form_historial.is_valid():
            for form_adjunto in formset_adjunto:
                if form_adjunto.cleaned_data.get('DELETE', False) and hasattr(form_adjunto.instance, 'pk'):
                    if form_adjunto.instance.id is not None or form_adjunto.instance.pk is not None:
                        form_adjunto.instance.delete()
                    continue
                form_adjunto.instance.requisicion = requisicion
                if not form_adjunto.cleaned_data.get('archivo', False):
                    continue
                form_adjunto.save()

            messages.success(request, _("Se ha editado la requisicion No.{} exitosamente".format(requisicion.id)))
            return redirect(reverse('compras:adjuntar_archivos_requisicion', args=(requisicion.id, )))

        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))

    else:
        form_historial = FormularioObservacionHistorial()
        formset_adjunto = AdjuntoFormset(queryset=requisicion.adjunto_set.all())

    data = {'formset_adjunto': formset_adjunto, 'form': form_historial}

    return render(request, 'compras/adjuntar_archivos_requisicion.html', data)
