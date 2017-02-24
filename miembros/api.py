from django.contrib.auth.decorators import permission_required, PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .forms import DesvincularLiderGrupoForm
from .models import Miembro
from common.decorators import login_required_api
from common import constants
from common.api import get_error_forms_to_json


@login_required_api
@permission_required('miembros.es_administrador', raise_exception=True)
def desvincular_lider_grupo_api(request, pk):
    """
    Desvincula a un lider de un grupo de amistad
    """

    miembro = get_object_or_404(Miembro.objects.iglesia(request.iglesia), pk=pk)

    if request.method == 'POST':
        form = DesvincularLiderGrupoForm(iglesia=request.iglesia, data=request.POST)

        if form.is_valid():
            form.desvincular_lider()
            return JsonResponse({'url': reverse('miembros:editar_perfil', args=(miembro.id, ))})
        else:
            errors = get_error_forms_to_json(form)
            return JsonResponse(errors, safe=False)

    raise PermissionDenied
