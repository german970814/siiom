from .models import Grupo

import datetime


def convertir_lista_a_queryset(lista_grupos):
    """
    Permite convertir una lista de grupos a un queryset según su pk.
    """

    lista_ids = [grupo.pk for grupo in lista_grupos]
    return Grupo.objects.filter(pk__in=lista_ids)


def reunion_reportada(fecha, grupo, discipulado=False):
    """Retorna verdadero si la existe una reunion en la fecha dada"""
    ini_semana = fecha - datetime.timedelta(days=fecha.isoweekday() - 1)
    fin_semana = fecha + datetime.timedelta(days=7 - fecha.isoweekday())

    if discipulado:  # discipulado
        reunion = grupo.reuniondiscipulado_set.filter(fecha__gte=ini_semana, fecha__lte=fin_semana)
    else:  # gar
        reunion = grupo.reuniongar_set.filter(fecha__gte=ini_semana, fecha__lte=fin_semana)

    return reunion.exists()


def obtener_fechas_semana(fecha):
    """
    Retorna las fechas de la semana de lunes a domingo a partir de una fecha
    """
    inicio_semana = fecha - datetime.timedelta(days=fecha.isoweekday() - 1)
    fin_semana = fecha + datetime.timedelta(days=7 - fecha.isoweekday())

    _fechas = []

    while inicio_semana <= fin_semana:
        _fechas.append(inicio_semana)
        inicio_semana += datetime.timedelta(days=1)

    return _fechas
