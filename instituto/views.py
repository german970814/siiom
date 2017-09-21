from django.forms import inlineformset_factory
from django.contrib import messages
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect

from .models import (
    Curso, Matricula, Modulo, Sesion
)
from .forms import (
    FormularioMateria, FormularioModulo, FormularioSesion
)

__author__ = 'German Alzate'


def crear_materia(request):
    """
    Vista de creación de una materia, también sirve para crear modulos y sesiones.
    """

    data = {}

    ModuloFormSet = inlineformset_factory(
        Materia, Modulo, fk_name='materia',
        form=FormularioModulo, min_num=1, extra=1,
        validate_min=True, can_delete=False
    )

    if request.method == 'POST':
        formulario_materia = FormularioMateria(request.POST)
        if formulario_materia.is_valid():
            materia = formulario_materia.save(commit=False)
            formulario_modulo 
            materia.save()
    else:
        formulario_materia = FormularioMateria()

    data['formulario_materia'] = formulario_materia

    return render(request, 'istituto/crear_materia.html', data)


def lista_estudiantes_sesion(request):
    from django.shortcuts import render
    return render(request, 'academia/lista_estudiantes_sesion.html', {})
