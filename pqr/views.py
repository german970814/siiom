# Django Package
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.conf import settings

# Locale Apps
from .models import Caso  # , Invitacion
from .forms import FormularioCaso, FormularioAgregarMensaje, FormularioAgregarIntegrante
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
            miembro = get_object_or_404(Miembro, usuario=request.user)
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
                    caso.save()
                else:
                    enviar_email_verificacion(request, caso)
            except Exception as e:
                if settings.DEBUG:
                    from django.http import HttpResponse
                    return HttpResponse(e, content_type='text/plain')
                pass
            messages.success(request, _('Se ha enviado un correo de verificación'))
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

    casos = Caso.objects.filter(valido=True).exclude(cerrado=True)

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

    caso.empleado_cargo.ultimo_mensaje = caso.empleado_cargo.comentario_set.filter(caso=caso).last().mensaje

    initial = {'caso': caso.id, 'empleado': empleado.id}
    initial_for_integrante = {'caso': caso.id, 'emisor': empleado.id}

    if request.method == 'POST':
        form = FormularioAgregarMensaje(data=request.POST, initial=initial)
        if mismo:
            form_integrante = FormularioAgregarIntegrante(data=request.POST, initial=initial_for_integrante)

        if 'integrante' in request.POST:
            if form_integrante.is_valid():
                receptor = form_integrante.get_receptor()
                invitacion = form_integrante.save(commit=False)
                invitacion.receptor = receptor
                invitacion.save()
                return redirect(reverse('pqr:ver_bitacora_caso', args=(caso.id, )))
            else:
                pass
        else:
            if form.is_valid():
                form.save()
                return redirect(reverse('pqr:ver_bitacora_caso', args=(caso.id, )))
            else:
                pass
    else:
        form = FormularioAgregarMensaje(initial=initial)
        if mismo:
            form_integrante = FormularioAgregarIntegrante(initial=initial_for_integrante)
        else:
            form_integrante = None

    data = {'caso': caso, 'empleado': empleado, 'form': form, 'form_integrante': form_integrante}

    return render(request, 'pqr/ver_bitacora_caso.html', data)
