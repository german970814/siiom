# Django Packages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.db import transaction
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required

# Third Apps
from waffle.decorators import waffle_switch

# Locale Apps
from .forms import (
    FormularioSolicitudRequisicion, FormularioDetalleRequisicion, FormularioAdjunto,
    FormularioRequisicionesCompras, FormularioObservacionHistorial
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
                url = """
                    <a class='alert-link' href='%s'>Ver Mis Requisiciones</a>
                    """ % reverse_lazy('compras:ver_requisiciones_empleado')
                requisicion.save()
                formset_adjunto.save()
                formset_detalles.save()
                if empleado.jefe_departamento:
                    historial = requisicion.crear_historial(empleado=empleado, estado=Historial.APROBADA)
                    historial.save()
                messages.success(request, _("Se ha creado la requisicion con éxito" + url))
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
                url = """
                    <a class='alert-link' href='%s'>Ver Mis Requisiciones</a>
                    """ % reverse_lazy('compras:ver_requisiciones_empleado')
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
                messages.success(request, _("Se ha editado la requisicion con éxito " + url))
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

    data = {}

    if request.method == 'POST':
        form = FormularioRequisicionesCompras(data=request.POST)
        if form.is_valid():
            requisicion = Requisicion.objects.get(id=form.cleaned_data['id_requisicion'])
            if 'aprobar' in request.POST:
                if form.cleaned_data['observacion'] != '':
                    historial = requisicion.crear_historial(
                        empleado=empleado, estado=Historial.APROBADA,
                        observacion=form.cleaned_data['observacion']
                    )
                else:
                    historial = requisicion.crear_historial(
                        empleado=empleado, estado=Historial.APROBADA
                    )
                mensaje = 'aprobado'
                requisicion.estado = Requisicion.PROCESO
            elif 'rechazar' in request.POST:
                historial = requisicion.crear_historial(
                    empleado=empleado, estado=Historial.RECHAZADA,
                    observacion=form.cleaned_data['observacion']
                )
                mensaje = 'rechazado'
                requisicion.estado = Requisicion.ANULADA
            requisicion.save()
            historial.save()
            messages.success(
                request,
                _("Se ha {} la requisicion No.{} exitosamente").format(mensaje, requisicion.id)
            )
            return redirect('compras:ver_requisiciones_jefe_departamento')
        else:
            data['CLICK'] = form.cleaned_data['id_requisicion']
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))
    else:
        form = FormularioRequisicionesCompras()

    data['requisiciones'] = requisiciones
    data['form'] = form

    return render(request, 'compras/ver_requisiciones_jefe_departamento.html', data)


@waffle_switch('compras')
@permission_required('organizacional.es_compras')
def ver_requisiciones_compras(request):
    """
    Vista para ver las requisiciones que se han hecho desde un usuario de compras
    """
    empleado = request.user.empleado

    requisiciones = Requisicion.objects.aprobadas_jefe_departamento().order_by(
        '-fecha_ingreso').prefetch_related('historial_set')

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
                historial.save()
                messages.success(
                    request,
                    _("Se ha {} la requisición No.{} con exito".format(mensaje, requisicion.id))
                )
                return redirect('compras:ver_requisiciones_compras')
            else:
                messages.error(request, _("Ha hecho una peticion inválida"))
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

    # se obtiene la requisicion
    requisicion = get_object_or_404(Requisicion, pk=id_requisicion)

    # deja entrar siempre y cuando la solicitud no este anulada o terminada
    if requisicion.is_anulada or requisicion.estado == Requisicion.TERMINADA or \
       Requisicion.DATA_SET['administrativo'] == requisicion.get_rastreo():
        raise Http404

    # inicializa variable para saber si instnciar el formulario o no
    _historial_nuevo = False

    # se crea el formset que manejará los formularios de documentos adjuntos
    AdjuntoFormset = modelformset_factory(
        Adjunto, form=FormularioAdjunto, min_num=0, extra=1,
        validate_min=False, can_delete=True
    )

    if request.method == 'POST':
        # si la requisicion en su ultimo historial fue hecho por un usuario del area de compras
        if Requisicion.DATA_SET['administrativo'] == requisicion.get_rastreo():
            # se crea el formulario instanciado
            form_historial = FormularioObservacionHistorial(
                data=request.POST, instance=requisicion.historial_set.last()
            )
        else:
            # se crea un formulario nuevo
            form_historial = FormularioObservacionHistorial(data=request.POST)
            # se asigna true a la variable para indicar que es un formulario sin instancia
            _historial_nuevo = True

        # se instancia el formset
        formset_adjunto = AdjuntoFormset(
            data=request.POST, files=request.FILES,
            queryset=requisicion.adjunto_set.all(), prefix='adjunto_set'
        )

        # si todo es valido
        if formset_adjunto.is_valid() and form_historial.is_valid():
            url = """
                <a href='%s' class='alert-link'>Volver a la lista de Requisiciones</a>
                """ % reverse_lazy('compras:ver_requisiciones_compras')
            # ciclo encargado de borrar los documentos que seran eliminados y agregar los nuevos documentos
            for form_adjunto in formset_adjunto:
                # si el formulario tiene el DELETE en el post y si la instancia ya fue creada alguna vez
                if form_adjunto.cleaned_data.get('DELETE', False) and hasattr(form_adjunto.instance, 'pk'):
                    # si todo esta bien con el pk y id
                    if form_adjunto.instance.id is not None or form_adjunto.instance.pk is not None:
                        # se borra el documento que se pidio desde la vista
                        form_adjunto.instance.delete()
                    continue
                # si no, crea el documento y le asigna la requisicion
                form_adjunto.instance.requisicion = requisicion
                # si no tiene archivo no lo guarda
                if not form_adjunto.cleaned_data.get('archivo', False):
                    continue
                # de el caso contrario guarda el formulario con el nuevo archivo
                form_adjunto.save()

            historial = form_historial.save(commit=False)
            # Si es nuevo y tiene alguna observacion
            # si no tiene observacion tiene la opcion de darle en aceptar desde la vista de lista
            if _historial_nuevo and historial.observacion != '':
                # se crea el hitorial
                historial.empleado = request.user.empleado
                historial.requisicion = requisicion
                historial.estado = Historial.APROBADA

            # siempre y cuando sea un historial completo se guarda
            if hasattr(historial, 'requisicion'):
                historial.save()

            messages.success(
                request,
                _("Se ha editado la requisicion No.{} exitosamente ".format(requisicion.id) + url)
            )
            if Requisicion.DATA_SET['compras']:
                return redirect(reverse('compras:adjuntar_archivos_requisicion', args=(requisicion.id, )))
            return redirect(reverse('compras:ver_requisiciones_compras'))

        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))

    else:
        # if requisicion.historial_set.last().observacion != '':
        # se verifica quien fue el ultimo en hacer algo con la requisicion para instanciar o no el formulario
        if Requisicion.DATA_SET['administrativo'] == requisicion.get_rastreo():
            from django.http import HttpResponse
            return HttpResponse(requisicion.historial_set.last().empleado)
            form_historial = FormularioObservacionHistorial(
                instance=requisicion.historial_set.last()
            )
        # si no, no se instancia el formulario
        else:
            form_historial = FormularioObservacionHistorial()
        # se instancia el formulario de archivos adjuntos
        formset_adjunto = AdjuntoFormset(queryset=requisicion.adjunto_set.all(), prefix='adjunto_set')

    data = {'formset_adjunto': formset_adjunto, 'form': form_historial, 'requisicion': requisicion}

    return render(request, 'compras/adjuntar_archivos_requisicion.html', data)


@waffle_switch('compras')
@login_required
def ver_requisiciones_jefe_administrativo(request):
    """
    Vista que lista las requisiciones que fueron aprobadas por los usuarios de compras
    y que se encuentran para que el jefe administrativo pueda aprobarlas o rechazarlas
    """

    requisiciones = Requisicion.objects.aprobadas_compras().distinct().order_by('-fecha_ingreso')
    empleado = request.user.empleado
    if not empleado.is_jefe_administrativo:
        return redirect('sin_permiso')

    data = {'requisiciones': requisiciones}

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
                historial = requisicion.crear_historial(
                    empleado=empleado, estado=Historial.RECHAZADA,
                    observacion=form.cleaned_data['observacion']
                )
                requisicion.estado = Requisicion.ANULADA
                requisicion.save()
                mensaje = 'rechazado'
            historial.save()
            messages.success(
                request,
                _("Se ha {} la requisición No.{} con exito".format(mensaje, requisicion.id))
            )
            return redirect('compras:ver_requisiciones_jefe_administrativo')
        else:
            data['CLICK'] = form.cleaned_data['id_requisicion']
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))
    else:
        form = FormularioRequisicionesCompras()

    data['form'] = form

    return render(request, 'compras/ver_requisiciones_jefe_administrativo.html', data)


@waffle_switch('compras')
@login_required
def ver_requisiciones_financiero(request):
    """
    Vista para ver las requisiciones que han llegado al sector financiero
    """
    pass
