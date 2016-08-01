# Django Packages
from django.shortcuts import render, redirect
from django.http import Http404
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.db import transaction
from django.core.urlresolvers import reverse
# from django.contrib.auth.decorators import permission_required


# Locale Apps
from .forms import FormularioSolicitudRequisicion, FormularioDetalleRequisicion, FormularioAdjunto
from .models import DetalleRequisicion, Requisicion, Adjunto


# @permission_required('')
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

    DetalleRequisicionFormSet = modelformset_factory(
        DetalleRequisicion, form=FormularioDetalleRequisicion,
        min_num=1, extra=0, validate_min=True, can_delete=True
    )

    AdjuntoFormset = modelformset_factory(
        Adjunto, form=FormularioAdjunto, min_num=0, extra=1,
        validate_min=False, can_delete=True
    )

    if request.method == 'POST':
        print("**********************************")
        print(request.POST)
        form = FormularioSolicitudRequisicion(data=request.POST, instance=requisicion)
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
