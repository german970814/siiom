import factory
import datetime

from grupos import models
from miembros.tests.factories import MiembroFactory


class GrupoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Grupo

    fechaApertura = factory.LazyFunction(datetime.datetime.now)
    lider1 = factory.SubFactory(MiembroFactory)
    horaDiscipulado = factory.Faker('time')
    horaGAR = factory.Faker('time')
    barrio_id = 1
    red_id = 1


class GrupoRaizFactory(GrupoFactory):
    red_id = None
