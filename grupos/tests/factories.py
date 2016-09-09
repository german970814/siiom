import factory
import datetime
from grupos import models
from miembros.tests.factories import MiembroFactory, BarrioFactory


class RedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Red
        django_get_or_create = ('nombre',)

    nombre = 'jovenes'


class GrupoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Grupo

    fechaApertura = factory.LazyFunction(datetime.datetime.now)
    lider1 = factory.SubFactory(MiembroFactory, lider=True)
    red = factory.SubFactory(RedFactory)
    horaDiscipulado = factory.Faker('time')
    horaGAR = factory.Faker('time')
    barrio = factory.SubFactory(BarrioFactory)


class GrupoRaizFactory(GrupoFactory):
    red = None


class GrupoHijoFactory(GrupoFactory):
    red = factory.LazyAttribute(lambda o: o.parent.red)
