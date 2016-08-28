#  Django Package
from django.db import models
from django.utils import timezone


class CasoManager(models.Manager):
    """
    Manager para el modelo de casos
    """

    def validos(self, *args, **kwargs):
        """
        Retorna los casos validos
        """
        return self.filter(valido=True, cerrado=False, *args, **kwargs)

    def nuevos(self):
        """
        Retorna los casos que apenas han ingresado al sistema y no tienen usuarios empleados a cargo
        """
        return self.validos(empleado_cargo=None, fecha_ingreso_habil__lte=timezone.now().date())

    def habiles(self):
        """
        Retorna los casos que han superado su fecha limite de acuerdo a los dias habiles establecidos
        """
        return self.validos()
