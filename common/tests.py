from django.contrib.auth.models import Group


ADMINISTRADOR = Group.objects.get(name__iexact='Administrador')
TESORERO = Group.objects.get(name__iexact='Tesorero')
COORDINADOR = Group.objects.get(name__iexact='Coordinador')
LIDER = Group.objects.get(name__iexact='Lider')


def liderTest(user):
    return user.is_authenticated() \
        and LIDER in user.groups.all()


def agenteTest(user):
    return user.is_authenticated() \
        and Group.objects.get(name__iexact='Agente') in user.groups.all()


def editarMiembroTest(user):
    return user.is_authenticated() \
        and user.has_perm("miembros.puede_editar_miembro")


def llamdaAgenteTest(user):
    return user.is_authenticated() \
        and user.has_perm("miembros.llamada_agente")


def agregarVisitanteTest(user):
    return user.is_authenticated() \
        and user.has_perm("miembros.puede_agregar_visitante")


def cumplimientoPasosTest(user):
    return user.is_authenticated() \
        and user.has_perm("miembros.cumplimiento_pasos")


def asignarGrupoTest(user):
    return (
        user.is_authenticated() and
        (Group.objects.get(name__iexact='Agente') in user.groups.all() or
         ADMINISTRADOR in user.groups.all())
    )


def miembroTest(user):
    return (
        user.is_authenticated() and
        (Group.objects.get(name__iexact='Maestro') in user.groups.all() or
         LIDER in user.groups.all() or Group.objects.get(name__iexact='Agente') in user.groups.all() or
         Group.objects.get(name__iexact='Receptor') in user.groups.all() or
         ADMINISTRADOR in user.groups.all() or user.has_perm('organizacional.es_administrador_sgd') or
         user.has_perm('organizacional.buscar_registros') or user.has_perm('gestion_documental.add_registro'))
    )


def receptorTest(user):
    return user.is_authenticated() \
        and Group.objects.get(name__iexact='Receptor') in user.groups.all()


def adminTest(user):
    return user.is_authenticated() \
        and ADMINISTRADOR in user.groups.all()


def verGrupoTest(user):
    return (
        user.is_authenticated() and
        (Group.objects.get(name__iexact='Lider') in user.groups.all() or
         ADMINISTRADOR in user.groups.all())
    )


def receptorAdminTest(user):
    return (
        user.is_authenticated() and
        (Group.objects.get(name__iexact='Receptor') in user.groups.all() or
         ADMINISTRADOR in user.groups.all())
    )


def PastorAdminTest(user):
    return (
        user.is_authenticated() and
        (Group.objects.get(name__iexact='Pastor') in user.groups.all() or
         ADMINISTRADOR in user.groups.all())
    )


def maestroTest(user):
    return user.is_authenticated() \
        and Group.objects.get(name__iexact='Maestro') in user.groups.all()


def adminMaestroTest(user):
    return (
        user.is_authenticated() and
        (ADMINISTRADOR in user.groups.all() or
         Group.objects.get(name__iexact='Maestro') in user.groups.all())
    )


def liderAdminTest(user):
    return (
        user.is_authenticated() and
        (LIDER in user.groups.all() or
         ADMINISTRADOR in user.groups.all())
    )


def agenteAdminTest(user):
    return (
        user.is_authenticated() and
        (Group.objects.get(name__iexact='Agente') in user.groups.all() or
         ADMINISTRADOR in user.groups.all())
    )


def tesorero_administrador_test(user):
    grupos = user.groups.all()
    return user.is_authenticated() and TESORERO in grupos or ADMINISTRADOR in grupos


def admin_tesorero_coordinador_test(user):
    grupos = user.groups.all()
    return user.is_authenticated() and TESORERO in grupos or ADMINISTRADOR in grupos or COORDINADOR in grupos
