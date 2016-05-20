from django.contrib.auth.models import Group


def liderTest(user):
    return user.is_authenticated() \
        and Group.objects.get(name__iexact='Lider') in user.groups.all()


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
    return user.is_authenticated()\
        and (Group.objects.get(name__iexact='Agente') in user.groups.all()
        or Group.objects.get(name__iexact='Administrador') in user.groups.all())


def miembroTest(user):
    return user.is_authenticated() \
        and (Group.objects.get(name__iexact='Maestro') in user.groups.all()
        or Group.objects.get(name__iexact='Lider') in user.groups.all()
        or Group.objects.get(name__iexact='Agente') in user.groups.all()
        or Group.objects.get(name__iexact='Receptor') in user.groups.all()
        or Group.objects.get(name__iexact='Administrador') in user.groups.all())


def receptorTest(user):
    return user.is_authenticated() \
        and Group.objects.get(name__iexact='Receptor') in user.groups.all()


def adminTest(user):
    return user.is_authenticated() \
        and Group.objects.get(name__iexact='Administrador') in user.groups.all()


def verGrupoTest(user):
    return user.is_authenticated()\
        and (Group.objects.get(name__iexact='Lider') in user.groups.all()
        or Group.objects.get(name__iexact='Administrador') in user.groups.all())


def receptorAdminTest(user):
    return user.is_authenticated()\
        and (Group.objects.get(name__iexact='Receptor') in user.groups.all()
        or Group.objects.get(name__iexact='Administrador') in user.groups.all())


def PastorAdminTest(user):
    return user.is_authenticated()\
        and (Group.objects.get(name__iexact='Pastor') in user.groups.all()
        or Group.objects.get(name__iexact='Administrador') in user.groups.all())


def maestroTest(user):
    return user.is_authenticated() \
        and Group.objects.get(name__iexact='Maestro') in user.groups.all()


def adminMaestroTest(user):
    return user.is_authenticated() \
        and (Group.objects.get(name__iexact='Administrador') in user.groups.all()
        or Group.objects.get(name__iexact='Maestro') in user.groups.all())


def liderAdminTest(user):
    return user.is_authenticated() \
        and (Group.objects.get(name__iexact='Lider') in user.groups.all()
        or Group.objects.get(name__iexact='Administrador') in user.groups.all())


def agenteAdminTest(user):
    return user.is_authenticated() \
        and (Group.objects.get(name__iexact='Agente') in user.groups.all()
        or Group.objects.get(name__iexact='Administrador') in user.groups.all())
