# Django Package
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy

# Python Package
import hashlib
import random
from threading import Thread
from functools import wraps


def concurrente(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        hilo = Thread(target=function, args=args, kwargs=kwargs)
        hilo.daemon = True
        hilo.start()
        return hilo
    return decorator


def crear_llave():
    """
    Crea un Slug al azar
    """
    return hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:40]


@concurrente
def enviar_email_verificacion(request, caso):
    llave = crear_llave()
    caso.llave = llave
    caso.save()

    link = reverse_lazy('pqr:validar_caso', args=(llave, ))
    SENDER = 'iglesia@mail.webfaction.com'
    mensaje = """
        En hora buena!!!! \n
        Hemos recibido su petición satisfactioriamente, por favor para confirmar tu
        correo y solicitud, haz click en el siguiente enlace:\n
        http://%(domain)s%(link)s
    """

    send_mail(
        'Verificación de E-mail para PQR',
        mensaje % {'link': link, 'domain': request.META['HTTP_HOST']},
        SENDER,
        ('{}'.format(caso.email), ),
        fail_silently=False
    )
