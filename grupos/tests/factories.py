import factory
import datetime
from iglesias.tests.factories import IglesiaFactory
from miembros.tests.factories import BarrioFactory


class RedFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'grupos.Red'
        django_get_or_create = ('nombre',)

    nombre = 'jovenes'
    iglesia = factory.SubFactory(IglesiaFactory)


class HistorialEstadoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'grupos.HistorialEstado'

    estado = 'AC'
    fecha = factory.LazyFunction(datetime.datetime.now)
    grupo = None


class GrupoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'grupos.Grupo'

    horaGAR = factory.Faker('time')
    red = factory.SubFactory(RedFactory)
    horaDiscipulado = factory.Faker('time')
    barrio = factory.SubFactory(BarrioFactory)
    iglesia = factory.SubFactory(IglesiaFactory)
    fechaApertura = factory.LazyFunction(datetime.datetime.now)
    lider = factory.RelatedFactory('miembros.tests.factories.MiembroFactory', 'grupo_lidera', lider=True)
    historial = factory.RelatedFactory('grupos.tests.factories.HistorialEstadoFactory', 'grupo')


class GrupoRaizFactory(GrupoFactory):

    red = None
    parent = None


class GrupoHijoFactory(GrupoFactory):

    red = factory.LazyAttribute(lambda o: o.parent.red)
    lider = factory.RelatedFactory(
        'miembros.tests.factories.MiembroFactory', 'grupo_lidera',
        grupo=factory.LazyAttribute(lambda o: o.grupo_lidera.parent), lider=True
    )


class PredicaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'grupos.Predica'
        django_get_or_create = ('nombre',)

    nombre = 'la palabra de Dios'
    miembro = factory.SubFactory('miembros.tests.factories.MiembroFactory')


class ReunionGARFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'grupos.ReunionGAR'

    fecha = factory.LazyFunction(datetime.datetime.now)
    grupo = factory.SubFactory(GrupoFactory)
    numeroLideresAsistentes = 2
    predica = 'Palabra de Dios'
    numeroTotalAsistentes = 10
    numeroVisitas = 5
    ofrenda = 100000


class ReunionDiscipuladoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'grupos.ReunionDiscipulado'

    fecha = factory.LazyFunction(datetime.datetime.now)
    predica = factory.SubFactory(PredicaFactory)
    grupo = factory.SubFactory(GrupoFactory)
    numeroLideresAsistentes = 2
    ofrenda = 100000
