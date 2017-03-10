import calendar
import datetime


def get_date_for_report(fecha_inicial, fecha_final):
    """
    Funcion que a partir de una fecha inicial y otra fecha final, retorna una fecha entre estos dos parametros
    mientras que sea diferente de domingo, con esta se obtienen las fechas de los reportes.

    :returns:
        Una fecha a partir de otra, sin que pase de la semana en donde se encuentra la fecha inicial.

    :param fecha_inicial:
        Un objeto del tipo ``datetime.date`` o ``datetime.datetime`` a partir de el cual se empieza a buscar
        la fecha límite para el reporte.

    :param fecha_final:
        Un objeto del tipo ``datetime.date`` o ``datetime.datetime`` el cual es la fecha límite para devolver un
        dia de reporte.
    """
    lunes = 0
    martes = 1
    miercoles = 2
    jueves = 3
    viernes = 4
    sabado = 5
    domingo = 6

    while calendar.weekday(
        year=fecha_inicial.year, month=fecha_inicial.month, day=fecha_inicial.day
    ) != domingo and not fecha_inicial >= fecha_final:
        fecha_inicial += datetime.timedelta(days=1)
    return fecha_inicial
