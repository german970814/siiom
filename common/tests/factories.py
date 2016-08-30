import factory
from django.contrib.auth import models


class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'user%d' % n)
