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


def dias_to_horas(dia):
    """
    Retorna la cantidad de horas de acuerdo a los dias dados
    """
    if isinstance(dia, int):
        return dia * 24
    raise TypeError("variable 'dia' must be a int instance, %(var)s instance" % {'var': type(dia)})


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
        Hemos recibido su petición satisfactoriamente, por favor para confirmar tu
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


@concurrente
def enviar_email_success(request, caso):
    """
    Envia un email a el responsable de el caso, cuando todo este correcto
    """

    SENDER = 'iglesia@mail.webfaction.com'
    mensaje = """
        En hora buena!!! \n
        Hemos recibido su petición satisfactoriamente, Recibira su respuesta dentro
        de las siguientes %(HORAS)d horas hábiles, gracias por su atención
    """

    send_mail(
        'Hemos Recibido su solicitud exitosamente',
        mensaje % {'HORAS', dias_to_horas(caso.__class__.DIAS_PARA_EXPIRAR)},
        SENDER,
        ('{}'.format(caso.email), ),
        fail_silently=False
    )
