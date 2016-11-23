import factory
from django.contrib.auth import get_user_model, models


class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.LazyAttribute(lambda o: '%s@siiom.com' % o.username)
    password = factory.PostGenerationMethodCall('set_password', '123456')

    @factory.post_generation
    def user_permissions(self, created, extracted, **kwargs):
        if not created:
            return

        if extracted:
            for permission in extracted:
                self.user_permissions.add(models.Permission.objects.get(codename=permission))
