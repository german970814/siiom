from .models import Grupo


def convertir_lista_a_queryset(lista_grupos):
    """
    Permite convertir una lista de grupos a un queryset según su pk.
    """

    lista_ids = [grupo.pk for grupo in lista_grupos]
    return Grupo.objects.filter(pk__in=lista_ids)
