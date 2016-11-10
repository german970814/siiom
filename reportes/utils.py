from miembros.models import Miembro
import calendar
import datetime

# TODO eliminar
def listaGruposDescendientes_id(miembro):
    """Devuelve una lista con todos los ids de los grupos descendientes del grupo del miembro usado como parametro para ser
        usada en un choice field."""

    grupo = miembro.grupo_lidera
    if grupo:
        listaG = [grupo.id]
    else:
        listaG = []
    discipulos = list(miembro.discipulos())
    while len(discipulos) > 0:
        d = discipulos.pop(0)
        g = d.grupo_lidera
        if g:
            if g not in listaG:
                listaG.append(g.id)
            lid = Miembro.objects.filter(id__in=g.listaLideres())
            for l in lid:  # Se elimina los otros lideres de la lista de discipulos para que no se repita el grupo.
                if l in discipulos:
                    discipulos.remove(l)
        if d.discipulos():  # Se agregan los discipulos del miembro en la lista de discipulos.
            discipulos.extend(list(d.discipulos()))
    return listaG


def get_date_for_report(fecha_inicial, fecha_final):
    """
    Retorna una fecha a partir de otra, sin que pase de la semana en donde se encuentra la fecha inicial
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
