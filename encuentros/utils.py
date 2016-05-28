from threading import Thread
from miembros.models import TipoMiembro, Pasos, CumplimientoPasos, CambioTipo, Miembro
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
import datetime


def posponer_function(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


@posponer_function
def crear_miembros_con_encontristas(encontristas):
    tesorero_group = Group.objects.get(name__iexact='tesorero')
    coordinador_group = Group.objects.get(name__iexact='coordinador')
    tipo_miembro = TipoMiembro.objects.get(nombre__iexact='miembro')
    paso = Pasos.objects.get(nombre__iexact='encuentro')
    for encontrista in encontristas:
        if encontrista.asistio:
            try:
                Miembro.objects.get(cedula=encontrista.identificacion)
            except Miembro.DoesNotExist:
                nuevo_miembro = Miembro()
                if encontrista.segundo_nombre:
                    nombre = encontrista.primer_nombre + ' ' + encontrista.segundo_nombre
                else:
                    nombre = encontrista.primer_nombre
                nuevo_miembro.nombre = nombre
                nuevo_miembro.primerApellido = encontrista.primer_apellido
                if encontrista.segundo_apellido:
                    nuevo_miembro.segundoApellido = encontrista.segundo_apellido
                nuevo_miembro.cedula = encontrista.identificacion
                nuevo_miembro.genero = encontrista.genero
                nuevo_miembro.email = encontrista.email
                nuevo_miembro.grupo = encontrista.grupo
                nuevo_miembro.convertido = True
                nuevo_miembro.save()
                pasos = CumplimientoPasos()
                pasos.miembro = nuevo_miembro
                pasos.paso = paso
                pasos.fecha = datetime.date.today()
                pasos.save()
                cambio = CambioTipo()
                cambio.miembro = nuevo_miembro
                cambio.fecha = datetime.date.today()
                cambio.anteriorTipo = tipo_miembro
                cambio.nuevoTipo = tipo_miembro
                cambio.autorizacion = encontrista.encuentro.tesorero
                cambio.save()
    encuentro = encontrista.encuentro
    if tesorero_group in encuentro.tesorero.usuario.groups.all():
        encuentro.tesorero.usuario.groups.remove(tesorero_group)
        encuentro.tesorero.usuario.save()
    if coordinador_group in encuentro.coordinador.usuario.groups.all():
        encuentro.coordinador.usuario.groups.remove(coordinador_group)
        encuentro.coordinador.usuario.save()
    encuentro.estado = 'I'
    encuentro.save()


@posponer_function
def avisar_tesorero_coordinador_encuentro(tesorero, coordinador):
    tesorero_group = Group.objects.get(name__iexact='tesorero')
    coordinador_group = Group.objects.get(name__iexact='coordinador')
    if tesorero_group not in tesorero.usuario.groups.all():
        tesorero.usuario.groups.add(tesorero_group)
        tesorero.usuario.save()
    if coordinador_group not in coordinador.usuario.groups.all():
        coordinador.usuario.groups.add(coordinador_group)
        coordinador.save()


def solo_encuentros_miembro(request, encuentro):
    if not request.user.has_perm('miembros.es_administrador'):
        if request.user.has_perm('miembros.es_coordinador'):
            if encuentro not in Miembro.objects.get(usuario=request.user).encuentros_coordinador.all():
                return HttpResponseRedirect('/dont_have_permissions/')
        if request.user.has_perm('miembros.es_tesorero'):
            if encuentro not in Miembro.objects.get(usuario=request.user).encuentros_tesorero.all():
                return HttpResponseRedirect('/dont_have_permissions/')
    return None
