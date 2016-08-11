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
        ).exclude(estado=self.model.ANULADA).distinct()

    def aprobadas_compras(self):
        """
        Retorna un QuerySet con las requisiciones aprobadas por usuario de compras
        """
        # from .models import Historial
        # query1 = models.Q(historial__empleado__usuario__is_superuser=True)
        # query2 = models.Q(
        #     historial__empleado__usuario__groups__permissions__codename='organizacional.es_compras'
        # )
        # query3 = models.Q(
        #     historial__empleado__usuario__user_permissions__codename='organizacional.es_compras'
        # )
        # query = query1 | query2 | query3

        pre_query = self.annotate(
            num_historial=models.Count('historial')
        ).exclude(num_historial__lt=2, estado=self.model.ANULADA)

        # return self.filter(query, historial__estado=Historial.APROBADA).exclude(
        #     estado=self.model.ANULADA
        # ).distinct()

        return pre_query

    def aprobadas_jefe_administrativo(self):
        """
        Retorna un QuerySet con las requisiciones aprobadas por un jefe administrativo
        """
        return self.annotate(
            num_historial=models.Count('historial')
        ).exclude(num_historial__lt=3, estado=self.model.ANULADA)

    def aprobadas_jefe_financiero(self):
        """
        Retorna un Queryset con las requisiciones a las cuales un jefe financiero ha
        puesto una fecha de pago
        """
        return self.aprobadas_jefe_administrativo().exclude(fecha_pago=None)


class ParametrosManager(models.Manager):
    """
    Manager para la clase de parametros
    """

    def dias(self):
        """
        Devuelve el ultimo valor que tenga el campo de dias
        """
        return self.last().dias_habiles

    def tope(self):
        """
        Devuelve el ultimo valor que tenga en el campo de tope de monto
        """
        return self.last().tope_monto
