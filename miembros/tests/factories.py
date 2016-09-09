import factory
from common.tests.factories import UsuarioFactory
from miembros import models


class ZonaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Zona
        django_get_or_create = ('nombre',)

    nombre = 'zona 1'


class BarrioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Barrio
        django_get_or_create = ('nombre',)

    nombre = 'prado'
    zona = factory.SubFactory(ZonaFactory)


class MiembroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Miembro

    email = factory.Faker('email')
    nombre = factory.Faker('first_name', locale='es')
    cedula = factory.sequence(lambda n: '112343%02d' % n)
    primerApellido = factory.Faker('last_name', locale='es')

    class Params:
        lider = factory.Trait(
            usuario=factory.SubFactory(UsuarioFactory, user_permissions=('es_lider',))
        )
