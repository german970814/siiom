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
        # se sacan las requisiciones que tengan mas de 3 historiales y se excluyen las que esten en presidencia
        return self.annotate(
            num_historial=models.Count('historial')
        ).exclude(
            num_historial__lt=3, estado=self.model.ANULADA,
            id__in=self.en_presidencia().values_list('id', flat=True)  # presidencia es excluido
        )

    def aprobadas_jefe_financiero(self):
        """
        Retorna un Queryset con las requisiciones a las cuales un jefe financiero ha
        puesto una fecha de pago
        """
        # return self.aprobadas_jefe_administrativo().exclude(fecha_pago=None)
        from .models import DetalleRequisicion
        return self.filter(
            presupuesto_aprobado=self.model.SI,
            detallerequisicion__forma_pago__in=[DetalleRequisicion.EFECTIVO, DetalleRequisicion.DEBITO]
        ).exclude(estado=self.model.ANULADA)

    def en_presidencia(self):
        """
        Retorna un Queryset con las requisiciones que han superado un tope maximo definido
        por los parametros iniciales, siempre y cuando haya sido aprobada por un usuario jefe
        administrativo
        """
        from .models import Parametros
        # return self.aprobadas_jefe_administrativo().annotate(
        #     total_valores=models.Sum(models.F('detallerequisicion__total_aprobado'))
        # ).filter(total_valores__gte=Parametros.objects.tope()).exclude(estado=self.model.ANULADA)

        # antes de new feature dia 11 agosto
        # return self.annotate(
        #     total_valores=models.Sum('detallerequisicion__total_aprobado')
        # ).filter(
        #     total_valores__gte=Parametros.objects.tope()
        # ).exclude(estado__in=[self.model.ANULADA, self.model.TERMINADA])

        # se sacan las requisiciones que vallan a presidencia por superar cierto monto
        query_for_total = self.annotate(
            total_valores=models.Sum('detallerequisicion__total_aprobado')
        ).filter(total_valores__gte=Parametros.objects.tope()).values_list('id', flat=True)

        # se sacan las requisiciones que tengan 3 historiales
        query_for_historial = self.annotate(
            num_historial=models.Count('historial')
        ).filter(num_historial=3).values_list('id', flat=True)

        # se hace la intercepcion de los id, es decir las requisiciones que cumplan con las dos condiciones
        query = set(query_for_total) & set(query_for_historial)

        return self.filter(id__in=query)


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
