# Django Package
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
# from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory

# Locale Apps
from .models import Registro, Documento, PalabraClave
from .forms import FormularioRegistroDocumento, FormularioDocumentos


@transaction.atomic
def ingresar_registro(request):
    """"""

    # Define Formset
    DocumentosFormSet = inlineformset_factory(
        Registro, Documento, fk_name='registro', form=FormularioDocumentos,
        min_num=0, extra=1, validate_min=True, can_delete=False
    )

    if request.method == 'POST':
        form = FormularioRegistroDocumento(data=request.POST)

        if form.is_valid():
            registro = form.save(commit=False)
            form_documentos = DocumentosFormSet(request.POST, request.FILES, instance=registro)
            if form_documentos.is_valid():
                registro.save()
                palabras = form.cleaned_data['palabras']
                for palabra in palabras:
                    palabra_clave, created = PalabraClave.objects.get_or_create(nombre__iexact=palabra)
                    registro.palabras_claves.add(palabra_clave)
                registro.save()
                form_documentos.save()
                messages.success(request, _("Se ha creado"))
                return redirect('ingresar_registro')
            else:
                messages.error(request, _("se callo en el segundo"))
        else:
            form_documentos = DocumentosFormSet(queryset=Documento.objects.none())
            messages.error(request, _("todo mal llave"))
    else:
        form = FormularioRegistroDocumento()
        form_documentos = DocumentosFormSet(queryset=Documento.objects.none())

    data = {'form': form, 'form_documentos': form_documentos}

    return render(request, 'gestion_documental/ingresar_registro.html', data)


def api(request):
    import json
    from django.http import HttpResponse
    palabras = PalabraClave.objects.all()

    r = [p.nombre for p in palabras]

    return HttpResponse(json.dumps(r), content_type="application/javascript")
