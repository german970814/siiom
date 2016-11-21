# Django Package
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy

# Python Package
import hashlib
import random
from threading import Thread
from functools import wraps
import re


# CONSTANTS
SENDER = 'iglesia@mail.webfaction.com'


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
    global SENDER
    llave = crear_llave()
    caso.llave = llave
    caso.save()

    link = reverse_lazy('pqr:validar_caso', args=(llave, ))
    # SENDER = 'iglesia@mail.webfaction.com'
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
    global SENDER
    """
    Envia un email a el responsable de el caso, cuando todo este correcto
    """

    # SENDER = 'iglesia@mail.webfaction.com'
    mensaje = """
        ¡Hola!\n
        En nuestra casa estamos para servirle. Hemos recibido su solicitud, estaremos dando una pronta respuesta.\n
        Tenga en cuenta que su número de solicitud es: %(id_caso)d\n
        Para consultas respecto a esta solicitud, puede llamar al %(telefono)d o escribir a %(email)s\n
        Dios le bendiga.
    """

    send_mail(
        'Hemos Recibido su solicitud exitosamente',
        mensaje % {'telefono': 3688932, 'id_caso': caso.id, 'email': 'informacion@icasadelrey.org'},
        SENDER,
        ('{}'.format(caso.email), ),
        fail_silently=False
    )


@concurrente
def enviar_email_invitacion(request, caso, empleado, mensaje):
    """
    Envia un email a un invitado
    """
    global SENDER

    msj = """
        %(mensaje_from_form)s\n\n

        Por favor dirigete a http://%(domain)s/%(link)s para colaborar
    """

    data = {
        'mensaje_from_form': mensaje, 'domain': request.META['HTTP_HOST'],
        'link': reverse_lazy('pqr:ver_bitacora_caso', args=(caso.id, ))
    }

    send_mail(
        'Ha Sido invitado a Colaborar en un Caso de PQR',
        msj % data,
        SENDER,
        ('{}'.format(empleado.usuario.email), ),
        fail_silently=False
    )


def _format_string(string):
    """Retorna un string legible para ASCII"""

    REPLACES = (
        ('á', 'a'),
        ('é', 'e'),
        ('í', 'i'),
        ('ó', 'o'),
        ('ú', 'u'),
        ('à', 'a'),
        ('è', 'e'),
        ('ì', 'i'),
        ('ò', 'o'),
        ('ù', 'u'),
        ('ñ', 'n'),
        (' ', '_'),
    )

    match = re.compile(r'[a-zA-ZñÑáÁéÉíÍóÓúÚ\s0-9_]')
    string = ''.join(match.findall(string))
    for x in REPLACES:
        string = string.replace(x[0], x[1])
        string = string.replace(x[0].upper(), x[1].upper())
    return string
