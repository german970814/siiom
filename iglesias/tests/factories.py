import factory


class IglesiaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'iglesias.Iglesia'
        django_get_or_create = ('nombre',)

    nombre = 'siiom'
