from django.db import models


class RequisicionManager(models.Manager):
    """
    Manager para las requisiciones
    """

    def aprobadas_jefe_departamento(self):
        """
        Retorna un QuerySet con las requisiciones aprobadas por jefes
        """
        from .models import Historial
        return self.filter(
            historial__estado=Historial.APROBADA, historial__empleado__jefe_departamento=True
        )

    def aprobadas_compras(self):
        """
        Retorna un QuerySet con las requisiciones aprobadas por usuario de compras
        """
        from .models import Historial
        return self.filter(
            historial__estado=Historial.APROBADA,
            historial__empleado__usuario__user_permissions__codename='organizacional.es_compras'
        )
