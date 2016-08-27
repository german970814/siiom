# Django Package
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.conf import settings
from django.utils import timezone

# Locale Apps
from .models import Caso, Invitacion
from .forms import (
    FormularioCaso, FormularioAgregarMensaje, FormularioAgregarIntegrante, FormularioEliminarInvitacion,
)
from .utils import enviar_email_verificacion

# Apps
from miembros.models import Miembro
from organizacional.models import Empleado

# Third's Apps
from waffle.decorators import waffle_switch


@waffle_switch('pqr')
def nuevo_caso(request):
    """
    Vista de creacion de un nuevo caso, de queja pregunta o reclamo
    """

    # Se intenta obtener un miembro a partir de el request, o un empleado
    if request.user.is_authenticated():
        try:
            miembro = Miembro.objects.get(usuario=request.user)
            initial = {
                'nombre': '{} {}'.format(miembro.nombre, miembro.primerApellido),
                'identificacion': miembro.cedula, 'email': miembro.email,
                'telefono': miembro.telefono or miembro.celular or '',
                'direccion': miembro.direccion or ''
            }
        except Miembro.DoesNotExist:
            try:
                empleado = request.user.empleado
                initial = {
                    'nombre': '{} {}'.format(empleado.primer_nombre, empleado.primer_apellido),
                    'identificacion': empleado.cedula, 'email': empleado.usuario.email
                }
            except Empleado.DoesNotExist:
                initial = {}
    else:
        initial = {}

    if request.method == 'POST':
        form = FormularioCaso(data=request.POST, initial=initial)

        if form.is_valid():
            caso = form.save()
            try:
                if settings.DEBUG:
                    caso.valido = True
                    caso.fecha_ingreso_habil = caso.get_fecha_expiracion()
                    caso.save()
                else:
                    enviar_email_verificacion(request, caso)
            except Exception as e:
                if settings.DEBUG:
                    from django.http import HttpResponse
                    return HttpResponse(e, content_type='text/plain')
                pass
            # enviar_email_verificacion(request, caso)  # Comment this line when DEBUG is True
            messages.success(
                request,
                _("""Su solicitud ha sido enviada satisfactoriamente,
                     recibirá un correo de confirmación para verificar sus datos""")
            )
            return redirect(reverse_lazy('pqr:nuevo_caso'))
        else:
            messages.error(request, _('Ha ocurrido un error al enviar el formulario'))

    else:
        form = FormularioCaso(initial=initial)

    data = {'form': form}

    return render(request, 'pqr/nuevo_caso.html', data)


@waffle_switch('pqr')
def validar_caso(request, llave):
    """
    Vista que a partir de una llave o slug valida un modelo de Caso, solo asi puede este
    ser visto por usuarios de servicio al cliente
    """

    caso = get_object_or_404(Caso, llave=llave)

    if not caso.valido and not caso._validacion_expirada():
        caso.valido = True
        caso.fecha_registro = timezone.now()
        caso.fecha_ingreso_habil = caso.get_fecha_expiracion().date()
        caso.save()
        data = {'caso': caso}
        return render(request, 'pqr/validar_caso.html', data)
    raise Http404


@waffle_switch('pqr')
@login_required
def ver_casos_servicio_cliente(request):
    """
    Vista para listar los casos que hayan sido validados por correo
    """

    casos = Caso.objects.nuevos()

    data = {'casos': casos}

    return render(request, 'pqr/ver_casos_servicio_cliente.html', data)


@waffle_switch('pqr')
@login_required
def ver_bitacora_caso(request, id_caso):
    """
    Vista para ver la bitacora de un caso de pqr
    """

    try:
        empleado = request.user.empleado
    except Empleado.DoesNotExist:
        raise Http404

    caso = get_object_or_404(Caso, id=id_caso)

    if not caso.empleado_cargo:
        caso.empleado_cargo = empleado
        caso.save()
    else:
        if not caso.integrantes.filter(id=empleado.id).exists() and caso.empleado_cargo != empleado:
            raise Http404

    mismo = False
    if empleado == caso.empleado_cargo:
        mismo = True

    if caso.empleado_cargo.comentario_set.exists():
        caso.empleado_cargo.ultimo_mensaje = caso.empleado_cargo.comentario_set.filter(caso=caso).last().mensaje

    integrantes = caso.integrantes.all()
    for integrante in integrantes:
        integrante.invitacion = integrante.invitaciones_recibidas.filter(caso=caso).last()
        if integrante.comentario_set.filter(caso=caso).exists():
            integrante.mensaje = integrante.comentario_set.filter(caso=caso).last().mensaje

    initial = {'caso': caso.id, 'empleado': empleado.id}
    initial_for_integrante = {'caso': caso.id, 'emisor': empleado.id}

    data = {'caso': caso, 'empleado': empleado, 'integrantes': integrantes}

    if request.method == 'POST':
        form = FormularioAgregarMensaje(data=request.POST, initial=initial)
        if mismo:
            form_integrante = FormularioAgregarIntegrante(
                data=request.POST, initial=initial_for_integrante, prefix='integrante'
            )
            form_eliminar_integrante = FormularioEliminarInvitacion(
                data=request.POST, query=caso.integrantes.all(), prefix='eliminar'
            )

        if 'integrante' in request.POST:
            if form_integrante.is_valid():
                receptor = form_integrante.get_receptor()
                invitacion = form_integrante.save(commit=False)
                invitacion.receptor = receptor
                invitacion.save()
                caso.integrantes.add(receptor)
                return redirect(reverse('pqr:ver_bitacora_caso', args=(caso.id, )))
            else:
                # print(form_integrante.errors)
                data['click'] = True
        elif 'eliminar_integrante' in request.POST:
            if form_eliminar_integrante.is_valid():
                empleado_eliminar = form_eliminar_integrante.cleaned_data['integrante']
                caso.integrantes.remove(empleado_eliminar)
                Invitacion.objects.get(caso=caso, receptor=empleado_eliminar).delete()
                return redirect(reverse('pqr:ver_bitacora_caso', args=(caso.id, )))
            else:
                data['click2'] = True
        else:
            if form.is_valid():
                form.save()
                return redirect(reverse('pqr:ver_bitacora_caso', args=(caso.id, )))
            else:
                # print(form.errors)
                pass
    else:
        form = FormularioAgregarMensaje(initial=initial)
        if mismo:
            form_integrante = FormularioAgregarIntegrante(initial=initial_for_integrante, prefix='integrante')
            form_eliminar_integrante = FormularioEliminarInvitacion(query=caso.integrantes.all(), prefix='eliminar')
        else:
            form_integrante = None
            form_eliminar_integrante = None

    data['form'] = form
    data['form_integrante'] = form_integrante
    data['form_eliminar_integrante'] = form_eliminar_integrante
    data['mismo'] = mismo

    return render(request, 'pqr/ver_bitacora_caso.html', data)


@waffle_switch('pqr')
@login_required
def ver_casos_jefe_comercial(request):
    """
    Vista para ver los casos que han superado el limite de 72 horas, y que deben ser revisados por un jefe
    de departamento
    """

    try:
        empleado = request.user.empleado
        if not empleado.is_jefe_comercial:
            raise Http404
    except Empleado.DoesNotExist:
        raise Http404
    casos = Caso.objects.habiles()
    data = {'casos': casos}

    return render(request, 'pqr/ver_casos_jefe_comercial.html', data)


@waffle_switch('pqr')
@login_required
def ver_casos_empleado(request):
    """
    Vista para ver los casos en los cuales un empleado es participante
    """

    try:
        empleado = request.user.empleado
    except Empleado.DoesNotExist:
        raise Http404

    _casos_1 = empleado.casos_cargo.filter(cerrado=False)
    _casos_2 = empleado.casos_implicado.filter(cerrado=False)

    casos = _casos_1 | _casos_2

    data = {'empleado': empleado, 'casos': casos}

    return render(request, 'pqr/ver_casos_empleado.html', data)
