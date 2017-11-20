from django.db import models, transaction
from django.db.models.query import QuerySet
from django.contrib.auth.models import Permission


class MiembroQuerySet(models.QuerySet):
    """
    Queryset personalizado para los miembros.
    """

    def lideres(self):
        """
        :returns:
            Un queryset con los lideres de una iglesia.
            Los lideres son los miembros que tengan permiso de lider.
        """

        permiso = Permission.objects.get(codename='es_lider')
        return self.filter(models.Q(usuario__groups__permissions=permiso) | models.Q(usuario__user_permissions=permiso))

    def red(self, red):
        """
        :returns:
            Un queryset con los miembros filtrados por la red a la cual pertenece el grupo al que asisten como
            miembros.

        :param red:
            La red a partir la cual se hara el filtro.
        """

        return self.filter(grupo__red=red)


class MiembroManager(models.Manager.from_queryset(MiembroQuerySet)):
    """
    Manager para los el modelo de Miembros.
    """

    def trasladar_lideres(self, lideres, nuevo_grupo):
        """
        Traslada los lideres ingresados, del grupo al que lideran actualmente a un nuevo grupo. Si el grupo actual
        se queda sin lideres, se fusiona el grupo actual con el nuevo grupo.

        :param lideres:
            Un Queryset de lideres a los cuales se les va a trasladar.

        :param nuevo_grupo:
            El nuevo grupo a donde se quiere trasladar.
        """

        from grupos.models import Grupo

        if not isinstance(lideres, QuerySet):
            raise TypeError("lideres debe ser un QuerySet pero es un {}".format(lideres.__class__.__name__))

        grupos = list(Grupo.objects.filter(lideres__in=lideres).distinct())
        if len(grupos) == 0:
            raise ValueError("Los lideres ingresados deben liderar grupo")

        with transaction.atomic():
            lideres.update(grupo_lidera=nuevo_grupo, grupo=nuevo_grupo.get_parent())
            for grupo_actual in grupos:
                if grupo_actual != nuevo_grupo:
                    if not grupo_actual.lideres.exists():
                        grupo_actual.fusionar(nuevo_grupo)

    def lideres_disponibles(self):
        """
        :returns:
            Un queryset con los lideres que no se encuentran liderando grupo.
        """

        return self.filter(grupo_lidera__isnull=True).lideres()

    def lideres_red(self, red):
        """
        :returns:
            Un queryset con los lideres que lideran grupos de la red ingresada.

        :param red:
            La red a partir de la cual se quiere filtrar.
        """

        return self.filter(grupo_lidera__red=red).lideres()

    def visitas(self, **kwargs):
        """
        :returns:
            Un QuerySet con los miembros que son visitas.

        :param \*\*kwargs:
            Diccionario de argumentos que serán pasados al momento de filtrar.
        """

        from .models import TipoMiembro

        visita = TipoMiembro.objects.filter(nombre__iexact='visita')

        return self.annotate(tipos=models.Count('miembro_cambiado')).filter(
            tipos=1, miembro_cambiado__nuevoTipo=visita, **kwargs)
