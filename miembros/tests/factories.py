import factory

from miembros import models


class MiembroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Miembro

    email = factory.Faker('email')
    nombre = factory.Faker('first_name', locale='es')
    cedula = factory.sequence(lambda n: '112343%02d' % n)
    primerApellido = factory.Faker('last_name', locale='es')
