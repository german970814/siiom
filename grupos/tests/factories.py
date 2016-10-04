import factory
import datetime
from grupos import models
from miembros.tests.factories import BarrioFactory


class RedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Red
        django_get_or_create = ('nombre',)

    nombre = 'jovenes'


class GrupoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Grupo

    horaGAR = factory.Faker('time')
    red = factory.SubFactory(RedFactory)
    horaDiscipulado = factory.Faker('time')
    barrio = factory.SubFactory(BarrioFactory)
    fechaApertura = factory.LazyFunction(datetime.datetime.now)
    lider = factory.RelatedFactory('miembros.tests.factories.MiembroFactory', 'grupo_lidera', lider=True)


class GrupoRaizFactory(GrupoFactory):
    red = None
    parent = None


class GrupoHijoFactory(GrupoFactory):
    red = factory.LazyAttribute(lambda o: o.parent.red)
    lider = factory.RelatedFactory(
        'miembros.tests.factories.MiembroFactory', 'grupo_lidera',
        grupo=factory.LazyAttribute(lambda o: o.grupo_lidera.parent), lider=True
    )
