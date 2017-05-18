from django.contrib.auth.decorators import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .forms import DesvincularLiderGrupoForm, ResetearContrasenaAdminForm
from .models import Miembro
from .decorators import user_is_cabeza_red
from common.decorators import login_required_api
from common import constants
from common.api import get_error_forms_to_json


@login_required_api
@user_is_cabeza_red  # No hay soporte con JSON
def desvincular_lider_grupo_api(request, pk):
    """
    Desvincula a un lider de un grupo de amistad
    """

    miembro = get_object_or_404(Miembro, pk=pk)

    if request.method == 'POST':
        form = DesvincularLiderGrupoForm(data=request.POST)

        if form.is_valid():
            form.desvincular_lider()
            return JsonResponse({'url': reverse('miembros:editar_perfil', args=(miembro.id, ))})
        else:
            errors = get_error_forms_to_json(form)
            return JsonResponse(errors, safe=False)

    return JsonResponse({constants.RESPONSE_CODE: constants.RESPONSE_DENIED})


# @permission_required('miembros.es_administrador', raise_exception=True)
@login_required_api
def resetear_contrasena(request):
    """Permite a un administrador resetear la contraseña de un miembro."""

    if request.method == 'POST':
        form = ResetearContrasenaAdminForm(request.POST)

        if form.is_valid():
            form.resetear()
            return JsonResponse({constants.RESPONSE_CODE: constants.RESPONSE_SUCCESS})

        errors = get_error_forms_to_json(form)
        return JsonResponse(errors, safe=False)

    return JsonResponse({constants.RESPONSE_CODE: constants.RESPONSE_DENIED})
