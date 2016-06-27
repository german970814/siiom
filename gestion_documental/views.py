# Django Package
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
# from django.forms.models import modelformset_factory

# Locale Apps
from .models import Registro, Documento, PalabraClave
from .forms import FormularioRegistroDocumento, FormularioDocumentos, FormularioBusquedaRegistro

# Apps
from waffle.decorators import waffle_switch
from organizacional.models import Area

# Python Package
import json


@waffle_switch('gestion_documental')
@permission_required('gestion_documental.add_registro')
@transaction.atomic
def ingresar_registro(request):
    """
    Vista de captura de datos para los registros del sistema de gestión.
    """

    # Define FormSet
    DocumentosFormSet = inlineformset_factory(
        Registro, Documento, fk_name='registro', form=FormularioDocumentos,
        min_num=1, extra=0, validate_min=True, can_delete=False
    )

    if request.method == 'POST':
        form = FormularioRegistroDocumento(data=request.POST)

        if form.is_valid():
            registro = form.save(commit=False)
            form_documentos = DocumentosFormSet(request.POST, request.FILES, instance=registro)
            # Si ambos documentos son validos
            if form_documentos.is_valid():
                registro.save()
                # Se extraen las palabras que vienen del formulario y se separan por coma en una lista
                palabras = form.cleaned_data['palabras'].split(',')
                # Se buscan las palabras recursivamente
                for palabra in palabras:
                    # Se busca, si no existe la palabra se crea
                    if palabra != '':
                        palabra_clave, created = PalabraClave.objects.get_or_create(
                            nombre__iexact=palabra, defaults={'nombre': palabra}
                        )

                        if palabra_clave not in registro.palabras_claves.all():
                            registro.palabras_claves.add(palabra_clave)
                # se guarda el registro
                registro.save()
                # Se guardan los documentos
                form_documentos.save()
                messages.success(request, _("Se ha creado el registro exitosamente"))
                # Todo Correcto
                return redirect('sgd:ingresar_registro')
            else:
                # Error en el formulario de documentos
                messages.error(request, _("Por favor verifique los documentos enviados"))
        else:
            # Error en el primer formulario del registro general
            form_documentos = DocumentosFormSet(queryset=Documento.objects.none(), data=request.POST)
            form_documentos.is_valid()
            messages.error(request, _("Se han encontrado errores en el formulario"))
    else:
        form = FormularioRegistroDocumento()
        form_documentos = DocumentosFormSet(queryset=Documento.objects.none())

    data = {'form': form, 'form_documentos': form_documentos}

    return render(request, 'gestion_documental/ingresar_registro.html', data)


def palabras_claves_json(request):
    """
    Vista que devuelve una lista con los nombres de las palabras claves para typeahead.js
    """

    palabras = PalabraClave.objects.all()
    response = [p.nombre for p in palabras]

    return HttpResponse(json.dumps(response), content_type="application/javascript")


@csrf_exempt
def area_tipo_documento_json(request):
    """
    Retorna los tipos de documentos pertenecientes a cada area
    """

    if request.method == 'POST':
        area = get_object_or_404(Area, pk=request.POST['id_area'])
        response = [{'id': tipo.id, 'tipo': tipo.nombre} for tipo in area.tipos_documento.all()]

        return HttpResponse(json.dumps(response), content_type="application/json")


@waffle_switch('gestion_documental')
@permission_required('gestion_documental.add_registro')
def busqueda_registros(request):
    """
    Vista para realizar la busqueda de registros
    """

    data = {}

    if request.method == 'POST':
        form = FormularioBusquedaRegistro(data=request.POST)

        if form.is_valid():
            tipo_documento = form.cleaned_data['tipo_documento']
            fecha_inicial = form.cleaned_data['fecha_inicial']
            fecha_final = form.cleaned_data['fecha_final']
            # Las palabras claves que vienen del formulario ya vienen en una lista
            palabras_claves = form.cleaned_data['palabras_claves']
            # Se dividen las palabras de la descripcion para hacer una mejor busqueda individual
            descripcion = form.cleaned_data['descripcion'].split(' ')

            # se buscan los registros en base a la fecha y al tipo de documento principalmente
            registros = Registro.objects.filter(
                fecha__range=(fecha_inicial, fecha_final),
                documentos__tipo_documento=tipo_documento,
            )

            # si hay palabras claves se filtran por las palabras claves
            if palabras_claves:
                registros = registros.filter(palabras_claves__in=palabras_claves)

            # queries = [Q(descripcion__icontains=descript) for descript in descripcion]

            # este seria el filtro por descripcion
            string_to_eval = ""
            link = "Q(descripcion__icontains='%s')"
            pipe = " | "

            # El siguiente ciclo se hace para enviar un queryset con "OR" de otro mododo
            # Quedaria sentencias para queries de " AND "

            # Ciclo para crear los querysets a partir de strings que luego seran evaluados
            for x in range(len(descripcion)):
                # cuando llegue al final del ciclo no agregara el pipe " | "
                if x == len(descripcion) - 1:
                    string_to_eval += (link % descripcion[x])
                # Mientras este en rango se agrega el pipe en la cadena para formar el " OR "
                else:
                    string_to_eval += (link % descripcion[x]) + pipe

            # registros = registros.filter(*queries)
            # Se evaluan los registros y se hace el filtro
            registros = registros.filter(eval(string_to_eval))

            # se añaden los registros a los datos que seran enviados a la vista,
            # que estan previamente cargados
            data['registros'] = registros

            messages.success(request, _("Se muestran los resultados"))
        else:
            # Ocurrieron errores
            messages.error(request, _("Ha ocurrido un error al enviar el formulario"))
    else:
        form = FormularioBusquedaRegistro()

    # se empaqueta el formulario
    data['form'] = form

    return render(request, 'gestion_documental/busqueda_registros.html', data)
