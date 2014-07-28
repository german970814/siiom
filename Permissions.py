#from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth.models import Group, Permission
#
#grupoAdministrador = Group(name='Administrador')
#grupoAdministrador.save()
#
#grupoLider = Group(name='Lider')
#grupoLider.save()
#
#grupoMaestro = Group(name='Maestro')
#grupoMaestro.save()
#
#grupoAgente  = Group(name='Agente')
#grupoAgente.save()
#
#grupoReceptor  = Group(name='Receptor')
#grupoReceptor.save()
#
#miembro_ct = ContentType.objects.get(app_label='Iglesia.miembros', model='Miembro')
#
#lider_agregar_miembro = Permission(name='agregar miembro', codename='agregar_miembro', content_type=miembro_ct)
#lider_editar_miembro = Permission(name='editar miembro', codename='editar_miembro', content_type=miembro_ct)
#lider_reasignar_miembro = Permission(name='agregar miembro', codename='agregar_miembro', content_type=miembro_ct)
#
#lider_reasignar_miembro.save()
#lider_agregar_miembro.save()
#lider_editar_miembro.save()
#
#grupoLider.permissions.add(lider_agregar_miembro)
#grupoLider.permissions.add(lider_editar_miembro)
#grupoLider.permissions.add(lider_reasignar_miembro)


#http://parand.com/say/index.php/2010/02/19/django-using-the-permission-system/
