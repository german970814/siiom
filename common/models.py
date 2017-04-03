from django.db import transaction


__all__ = ('UtilsModelMixin', )


class UtilsModelMixin:
    """
    Mixin de utilidades para los modelos.
    """

    def update(self, **options):
        """
        Actualiza los datos de el modelo.

        :param *options:
            Las opciones en clave:valor que van a ser cambiadas de los atributos del modelo.
        """

        keys = []
        with transaction.atomic():
            for key, value in options.items():
                setattr(self, key, value)
                keys.append(key)
            self.save(update_fields=keys)
