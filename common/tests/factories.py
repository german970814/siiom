import factory
from django.contrib.auth import models


class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.LazyAttribute(lambda o: '%s@siiom.com' % o.username)
    password = factory.PostGenerationMethodCall('set_password', '123456')
