import factory
from common.tests.factories import UsuarioFactory
from iglesias.tests.factories import IglesiaFactory
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

    grupo_lidera = None
    email = factory.Faker('email')
    iglesia = factory.SubFactory(IglesiaFactory)
    nombre = factory.Faker('first_name', locale='es')
    cedula = factory.sequence(lambda n: '112343%02d' % n)
    primerApellido = factory.Faker('last_name', locale='es')
    grupo = factory.LazyAttribute(lambda o: o.grupo_lidera.parent if o.grupo_lidera else None)

    class Params:
        lider = factory.Trait(
            usuario=factory.SubFactory(UsuarioFactory, user_permissions=['es_lider'])
        )
        admin = factory.Trait(
            usuario=factory.SubFactory(UsuarioFactory, user_permissions=['es_administrador'])
        )
