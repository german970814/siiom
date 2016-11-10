# decorators for views

# Django Package
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Functools
from functools import wraps


def login_empleado(*args, **kwargs):
    """
    Decorador para logear empleados
    """
    if isinstance(args[0], str):
        attribute = kwargs.pop('attribute', None) or args[0]

        def decorator(function_view):
            @wraps(function_view)
            @login_required
            def _wrapped_view(request, *args, **kwargs):
                if hasattr(request.user, 'empleado'):
                    if attribute is not None:
                        if not isinstance(attribute, str):
                            raise TypeError("Type of attribute must be a 'str', but is: %s" % attribute.__class__.__name__)
                        if getattr(request.user.empleado, attribute, False):
                            return function_view(request, *args, **kwargs)
                    else:
                        return function_view(request, *args, **kwargs)
                return redirect('sin_permiso')
            return _wrapped_view
        return decorator

    if callable(args[0]):
        @wraps(args[0])
        @login_required
        def wrapped_view(request, **kwargs):
            if hasattr(request.user, 'empleado'):
                return args[0](request, **kwargs)
            return redirect('sin_permiso')
        return wrapped_view
    else:
        return redirect('sin_permiso')


def codigo_funcionando(attribute=None):
    """
    Base, (difiere con el actual en que para poder usaarlo se debe mandar el decorador con '@decorator()' como funcion,
    mientras que el otro se envia como decorador normal, y puede recibir paramatros)
    """
    def decorator(function_view):
        @wraps(function_view)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'empleado'):
                if attribute is not None:
                    if not isinstance(attribute, str):
                        raise TypeError("Type of attribute must be a 'str', but is: %s" % attribute.__class__.__name__)
                    if getattr(request.user.empleado, attribute, False):
                        print("vine por aqui")
                        return function_view(request, *args, **kwargs)
                else:
                    return function_view(request, *args, **kwargs)
            return redirect('sin_permiso')
        return _wrapped_view
    return decorator
