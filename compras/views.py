"""

    Fecha Inicio Desarrollo: 1 Agosto 2016

    Desarrollado por Ingeniarte Soft.

    Trazabilidad de las requisiciones

    los siguientes son los pasos que sigue la trazabilidad de las requisiciones:

        - Un Usuario de Consulta hace una requisicion

        - Inicialmente esa requisicion llega al jefe de el departamento de usuario y es este
        jefe quien determina que ruta tomara esta peticion, de aprobarla, la peticion de la
        requisicion llegará a un usuario de el área de compras; de lo contrario, esta requisicion
        será anulada

        - Una vez un usuario jefe de el departamento aprueba una requisicion, esta, entra en
        estado de proceso y es direccionada a los usuarios que pertenezcan al area de compras,
        los cuales son los encargados de hacer las cotizaciones correspondientes a cada detalle
        de la requisición, a su vez pueden agregar comentarios y archivos adjuntos para complementar
        su trabajo con respecto a la requisicion, este usuario no puede darle un estado de rechazo a
        una requisicion. Una vez el usuario de compras haya terminado su proceso, puede darle paso a
        un Director administrativo

        - Un usuario administrativo es un empleado que es jefe de departamento y ese departamento
        puede tener cualquier nombre empezado por 'adminis', se sabe que es jefe de ese departamento
        si tiene un area relacionada con ese departamento, este jefe de departamento es el encargado
        de dar el ultimo visto acerca de la requisicion y tiene la potestad de aprobar o rechazar dicha
        requisicion

        - En caso de que el usuario administrativo apruebe la requisicion esta llega a los usuarios
        de el Departamento de financiamiento haciendo una primera escala a el jefe o director de este
        departamento, el cual debe poner a la requisicion una fecha de pago, y si quiere poner una forma
        en la cual el dinero será entregado, una vez realizado ese paso pasa a usuarios de el mismo
        departamento encargados de los pagos

        - Cuando El Director de el departamento de financiacion ha dado la fecha de pago de una requisicion
        esta llega a un usuario encargado de hacer el pago el cual al entregar el dinero le da un estado
        de terminado a la requisicion que viene dado a partir de otros tres posibles estados


"""

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
    FormularioRequisicionesCompras, FormularioObservacionHistorial, FormularioFechaPagoRequisicion,
    FormularioEstadoPago
)
from .models import DetalleRequisicion, Requisicion, Adjunto, Historial
from organizacional.models import Empleado

__author__ = 'German Alzate'


@waffle_switch('compras')
@login_required
@transaction.atomic
def crear_requisicion(request):
    """
    Vista para la creacion de requisiciones en el modulo de compras
    """
    try:
        # se obtiene el empleado
        empleado = request.user.empleado
    except:
        raise Http404

    # se crea el formset de los detalles de la requisicion
    DetalleRequisicionFormSet = inlineformset_factory(
        Requisicion, DetalleRequisicion, fk_name='requisicion',
        form=FormularioDetalleRequisicion, min_num=1, extra=4,
        validate_min=True, can_delete=False
    )

    # se crea el formset para los archivos adjuntos de la requisicion
    AdjuntoFormset = inlineformset_factory(
        Requisicion, Adjunto, fk_name='requisicion',
        form=FormularioAdjunto, min_num=0, extra=1,
        validate_min=True, can_delete=False
    )

    if request.method == 'POST':
        # se instancian los tres formularios
        form = FormularioSolicitudRequisicion(data=request.POST)
        # se crea una primera instancia de los formularios para que puedan ser validados
        formset_detalles = DetalleRequisicionFormSet(data=request.POST)
        formset_adjunto = AdjuntoFormset(request.POST, request.FILES)
        if form.is_valid():
            # se guarda la requisicion
            requisicion = form.save(commit=False)
            requisicion.empleado = empleado
            # se vuelven a instanciar los formularios para verificar que este todo válido
            formset_detalles = DetalleRequisicionFormSet(data=request.POST, instance=requisicion)
            formset_adjunto = AdjuntoFormset(request.POST, request.FILES, instance=requisicion)
            if formset_detalles.is_valid() and formset_adjunto.is_valid():
                # se crea una url para hacer la redireccion
                url = """
                    <a class='alert-link' href='%s'>Ver Mis Requisiciones</a>
                    """ % reverse_lazy('compras:ver_requisiciones_empleado')
                # si el empleado es jefe_departamento pero no es administrativo se crea un historial
                if empleado.jefe_departamento and not empleado.is_jefe_administrativo:
                    historial = requisicion.crear_historial(empleado=empleado, estado=Historial.APROBADA)
                    historial.save()
                    requisicion.estado = Requisicion.PROCESO
                # se crea la requisicion y se guardan los detalles y los adjuntos
                requisicion.save()
                formset_adjunto.save()
                formset_detalles.save()
                messages.success(request, _("Se ha creado la requisicion con éxito" + url))
                return redirect('compras:crear_requisicion')
            else:
                messages.error(request, _("Ha ocurrido un error al enviar el formulario"))
        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))

    else:
        # se instancian los 3 formularios
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
        # se obtiene la requisicion
        requisicion = Requisicion.objects.get(id=id_requisicion)
        if requisicion.estado != Requisicion.PENDIENTE:
            raise Http404
    except Requisicion.DoesNotExist:
        raise Http404
    # si el empleado no tiene los permisos se redirecciona a la pagina de sin permisos
    # si el empleado no fue quien realizó la requisicion
    empleado = requisicion.empleado
    try:
        if empleado != request.user.empleado:
            return redirect('sin_permiso')
    except Empleado.DoesNotExist:
        raise Http404

    # se crean los modelos de los formularios
    DetalleRequisicionFormSet = modelformset_factory(
        DetalleRequisicion, form=FormularioDetalleRequisicion,
        min_num=1, extra=0, validate_min=True, can_delete=True
    )

    AdjuntoFormset = modelformset_factory(
        Adjunto, form=FormularioAdjunto, min_num=0, extra=1,
        validate_min=False, can_delete=True
    )

    if request.method == 'POST':
        # se instancian los formularios de el POST
        form = FormularioSolicitudRequisicion(data=request.POST, instance=requisicion)
        # se les pone un prefijo a los formularios para que todo pueda trabajar bien
        formset_detalles = DetalleRequisicionFormSet(
            prefix='detallerequisicion_set',
            queryset=requisicion.detallerequisicion_set.all()
        )
        formset_adjunto = AdjuntoFormset(
            prefix='adjunto_set',
            queryset=requisicion.adjunto_set.all()
        )
        if form.is_valid():
            # si el formulario es valido se vuelven a instanciar los formularios [FORMSETS]
            formset_detalles = DetalleRequisicionFormSet(
                data=request.POST, prefix='detallerequisicion_set',
                queryset=requisicion.detallerequisicion_set.all()
            )
            formset_adjunto = AdjuntoFormset(
                data=request.POST, files=request.FILES, prefix='adjunto_set',
                queryset=requisicion.adjunto_set.all()
            )
            if formset_adjunto.is_valid() and formset_detalles.is_valid():
                # si todo está válido
                url = """
                    <a class='alert-link' href='%s'>Ver Mis Requisiciones</a>
                    """ % reverse_lazy('compras:ver_requisiciones_empleado')
                requisicion = form.save()
                # se guarda la requisicion y sus campos relacionados
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

    try:
        empleado = request.user.empleado
    except:
        raise Http404

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
    try:
        empleado = request.user.empleado
        if not empleado.jefe_departamento:
            return redirect('sin_permiso')
    except:
        raise Http404

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

    try:
        empleado = request.user.empleado
    except:
        raise Http404

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

    # se obtiene el usuario
    try:
        empleado = request.user.empleado
    except:
        raise Http404

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
                historial.empleado = empleado
                historial.requisicion = requisicion
                historial.estado = Historial.APROBADA

            # siempre y cuando sea un historial completo se guarda
            if hasattr(historial, 'requisicion'):
                historial.save()

            messages.success(
                request,
                _("Se ha editado la requisicion No.{} exitosamente ".format(requisicion.id) + url)
            )
            if Requisicion.DATA_SET['compras'] == requisicion.get_rastreo():
                return redirect(reverse('compras:adjuntar_archivos_requisicion', args=(requisicion.id, )))
            return redirect(reverse('compras:ver_requisiciones_compras'))

        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))

    else:
        # if requisicion.historial_set.last().observacion != '':
        # se verifica quien fue el ultimo en hacer algo con la requisicion para instanciar o no el formulario
        if Requisicion.DATA_SET['administrativo'] == requisicion.get_rastreo():
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
    try:
        empleado = request.user.empleado
        if not empleado.is_jefe_administrativo:
            return redirect('sin_permiso')
    except:
        raise Http404

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
    try:
        empleado = request.user.empleado
        if not empleado.is_jefe_financiero:
            raise Http404
    except Empleado.DoesNotExist:
        raise Http404

    requisiciones = Requisicion.objects.aprobadas_jefe_administrativo().distinct().order_by('-fecha_ingreso')
    data = {'requisiciones': requisiciones}

    if request.method == 'POST':
        pass
    else:
        pass

    return render(request, 'compras/ver_requisiciones_financiero.html', data)


@waffle_switch('compras')
@login_required
@transaction.atomic
def pre_pago_requisicion(request, id_requisicion):
    """
    Vista para darle a las requisiciones un pre-pago, indicando el dia que se debe pagar la factura
    y la forma de pago, antes de pasar a un usuario encargado de el pago
    """

    requisicion = get_object_or_404(Requisicion, pk=id_requisicion)
    try:
        empleado = request.user.empleado
        if not empleado.is_jefe_financiero or \
           Requisicion.DATA_SET['financiero'] != requisicion.get_rastreo() or requisicion.fecha_pago:
            raise Http404
    except Empleado.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioFechaPagoRequisicion(data=request.POST, instance=requisicion)

        if form.is_valid():
            requisicion = form.save()
            historial = requisicion.crear_historial(empleado=empleado, estado=Historial.APROBADA)
            requisicion.detallerequisicion_set.update(forma_pago=requisicion.form_pago)
            historial.save()
            messages.success(
                request,
                _("Se ha modificado la requisicion NO.{} exitosamente").format(requisicion.id)
            )
            return redirect('compras:ver_requisiciones_financiero')
        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))
    else:
        form = FormularioFechaPagoRequisicion(instance=requisicion)

    data = {'requisicion': requisicion, 'form': form}

    return render(request, 'compras/pre_pago_requisicion.html', data)


@waffle_switch('compras')
@login_required
def ver_requisiciones_usuario_pago(request):
    """
    Vista para listar las requisiciones que han aprobado los jefes de el departamento
    financiero
    """

    try:
        empleado = request.user.empleado
    except:
        raise Http404

    requisiciones = Requisicion.objects.aprobadas_jefe_financiero()

    data = {'requisiciones': requisiciones}

    return render(request, 'compras/ver_requisiciones_usuario_pago.html', data)


@waffle_switch('compras')
@login_required
def pagar_requisicion(request, id_requisicion):
    """
    Vista con la que acaba el proceso de trazabilidad, en la cual se le pone un estado
    de pago a la requisicion y se le da el estado de terminada, hecha por un usuario
    encargado de los pagos
    """

    try:
        empleado = request.user.empleado
    except:
        raise Http404

    requisicion = get_object_or_404(Requisicion, pk=id_requisicion)

    if Requisicion.DATA_SET['pago'] != requisicion.get_rastreo():
        raise Http404

    if request.method == 'POST':
        form = FormularioEstadoPago(data=request.POST, instance=requisicion)

        if form.is_valid():
            requisicion = form.save()
            requisicion.estado = Requisicion.TERMINADA
            requisicion.save()
            historial = requisicion.crear_historial(empleado=empleado, estado=Historial.APROBADA)
            historial.save()

            messages.success(
                request,
                _(
                    "Se ha culminado exitosamente el proceso de la requisicion No.{}".format(
                        requisicion.id
                    )
                )
            )
            return redirect('compras:ver_requisiciones_usuario_pago')

        else:
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))

    else:
        form = FormularioEstadoPago(instance=requisicion)

    data = {
        'form': form,
        'requisicion': requisicion
    }

    return render(request, 'compras/pagar_requisicion.html', data)
