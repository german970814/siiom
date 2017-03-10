from django.core import checks
from django.conf import settings

__author__ = 'German Alzate'


MIEMBRO_MIDDLEWARE_DOTTED_STRING = 'miembros.middleware.MiembroMiddleWare'
EMPLEADO_MIDDLEWARE_DOTTED_STRING = 'organizacional.middleware.EmpleadoMiddleWare'
IGLESIA_MIDDLEWARE_DOTTED_STRING = 'iglesias.middleware.IglesiaMiddleware'


@checks.register()
def iglesia_middleware_check(app_configs, **kwargs):
    """
    Check para el middleware de las iglesias, para que toda la app pueda trabajar de manera funcional.
    """

    errors = []

    if IGLESIA_MIDDLEWARE_DOTTED_STRING not in settings.MIDDLEWARE_CLASSES:
        errors.append(
            checks.Error(
                'No se encontró el middleware de iglesias.',
                hint=('Asegurate de que el middleware "%s" se encuentre en settings.MIDDLEWARE_CLASSES' %
                      IGLESIA_MIDDLEWARE_DOTTED_STRING),
                id='iglesias.E001'
            )
        )

    ordenes = {key: position for position, key in enumerate(settings.MIDDLEWARE_CLASSES)}

    if IGLESIA_MIDDLEWARE_DOTTED_STRING in ordenes:
        if MIEMBRO_MIDDLEWARE_DOTTED_STRING in ordenes:
            if ordenes[MIEMBRO_MIDDLEWARE_DOTTED_STRING] > ordenes[IGLESIA_MIDDLEWARE_DOTTED_STRING]:
                errors.append(
                    checks.Warning(
                        'Orden incorrecto en middlewares.',
                        hint=('Asegurate que el middleware "%s" esté después del middleware de "%s"' % (
                            IGLESIA_MIDDLEWARE_DOTTED_STRING, MIEMBRO_MIDDLEWARE_DOTTED_STRING
                        )),
                        id='iglesias.W001'
                    )
                )
        if EMPLEADO_MIDDLEWARE_DOTTED_STRING in ordenes:
            if ordenes[EMPLEADO_MIDDLEWARE_DOTTED_STRING] > ordenes[IGLESIA_MIDDLEWARE_DOTTED_STRING]:
                errors.append(
                    checks.Warning(
                        'Orden incorrecto en middlewares.',
                        hint=('Asegurate que el middleware "%s" esté después del middleware de "%s"' % (
                            IGLESIA_MIDDLEWARE_DOTTED_STRING, EMPLEADO_MIDDLEWARE_DOTTED_STRING
                        )),
                        id='iglesias.W002'
                    )
                )
        if EMPLEADO_MIDDLEWARE_DOTTED_STRING not in ordenes and MIEMBRO_MIDDLEWARE_DOTTED_STRING not in ordenes:
            errors.append(
                checks.Error(
                    'No se encotró el middleware de "miembros" ni "empleados"',
                    hint='Sin el middlware de miembros o empleados, el middleware de iglesias no podría funcionar adecuadamente'
                    'Asegurate de ubicarlos en el orden correcto.',
                    id='iglesias.E002'
                )
            )

    return errors
