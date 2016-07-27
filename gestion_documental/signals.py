# -*- coding: utf-8 -*-

# Django Package
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, post_delete

# Locale Apps
from .models import Documento, Registro

# Python Package
import os

__author__ = 'german'


class DocumentExistYetException(Exception):
    """
    Exception raised when document.archive object exists yet, then to been deleted
    """
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return repr(self.text)


@receiver(signal=post_save, sender=Documento)
@receiver(signal=post_save, sender=Registro)
def model_save(sender, **kwargs):
    # print("Se guardó {}".format(kwargs['instance'].__dict__))
    pass


# @receiver(signal=pre_delete, sender=Documento)
# def model_delete(sender, **kwargs):
#     instance = kwargs['instance']
    # if not instance.is_image:
    #     from .utils import get_route, get_filenames, CARPETA_PDF_TO_IMAGE
    #     ruta = get_route(instance.archivo) + CARPETA_PDF_TO_IMAGE
    #     for file in get_filenames(instance.archivo):
    #         if os.path.exists(ruta + file) and os.path.isfile(ruta + file):
    #             os.remove(ruta + file)
    # if os.path.exists(instance.archivo._get_path()) and os.path.isfile(instance.archivo._get_path()):
    #     # print("Se borra el archivo {}".format(instance.archivo.path))
    #     os.remove(instance.archivo._get_path())


@receiver(signal=post_delete, sender=Documento)
def model_post_delete(sender, **kwargs):
    instance = kwargs['instance']
    # if os.path.exists(instance.archivo.path):
    #     raise DocumentExistYetException('Documento Aún existe y no fue borrado')
    # pass
    if not instance.is_image:
        from .utils import get_route, get_filenames, CARPETA_PDF_TO_IMAGE
        _ruta = get_route(instance.archivo)
        if _ruta is not None:  # Mientras el archivo aún exista
            ruta = _ruta + CARPETA_PDF_TO_IMAGE
            for file in get_filenames(instance.archivo):
                if os.path.exists(ruta + file) and os.path.isfile(ruta + file):
                    os.remove(ruta + file)
    if os.path.exists(instance.archivo._get_path()) and os.path.isfile(instance.archivo._get_path()):
        # print("Se borra el archivo {}".format(instance.archivo.path))
        os.remove(instance.archivo._get_path())
