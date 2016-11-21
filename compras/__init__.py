from .models import Parametros

try:
    Parametros.objects.first().tope_monto
except AttributeError:
    raise Exception("No se han configurado los parametros")

# 1	Agosto 2016
__author__ = 'German Alzate'
default_app_config = 'compras.apps.ComprasConfig'
