from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def permisos_requeridos(*permisos):
    """
    Decorador para vistas que chequea si el usuario tiene algún permiso habilitado. Si no tiene ningún permiso se
    levanta la excepción PermissionDenied.
    """

    def chequear_permisos(user):
        for permiso in permisos:
            if user.has_perm(permiso):
                return True

        raise PermissionDenied
        return False

    return user_passes_test(chequear_permisos)
