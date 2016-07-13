# Django Package
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

# Locale Apps
# from gestion_documental.models import Documento
from .models import Area, Departamento, Empleado
from .forms import AreaForm, DepartamentoForm, EmpleadoForm

# Python Package
import json


@csrf_exempt
def areas_departamento_json(request):
    """
    Vista que devuelve una lista de areas a partir de un departamento en formato json
    """

    if request.method == 'POST':
        departamento = get_object_or_404(Departamento, pk=request.POST['id_departamento'])

        areas = Area.objects.filter(departamento__id=departamento.id)

        response = [{'id': area.id, 'area': area.nombre} for area in areas]

        return HttpResponse(json.dumps(response), content_type='application/json')


class AreaCreateView(CreateView):
    """CreateView for AreaCreateView"""
    model = Area
    form_class = AreaForm
    # fields = ['nombre', 'codigo']
    success_url = reverse_lazy('organizacional:crear_area')
    template_name = 'organizacional/crear_area.html'
    group_required = ['administrador sgd']

    def form_valid(self, form):
        messages.success(self.request, _("Se ha creado exitosamente el Area"))
        return super(AreaCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Ha ocurrido un error al enviar el formulario"))
        return super(AreaCreateView, self).form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        context['accion'] = _('Crear')
        # context['tipo'] = 'Area'
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )


class AreaUpdateView(UpdateView):
    """UpdateView for AreaUpdateView"""
    model = Area
    form_class = AreaForm
    # success_url = reverse_lazy('organizacional:editar_area')
    template_name = 'organizacional/crear_area.html'
    group_required = ['administrador sgd']

    def form_valid(self, form):
        messages.success(self.request, _("Se ha editado exitosamente el Área"))
        self.success_url = reverse_lazy('organizacional:editar_area', args=(form.instance.id, ))
        return super(AreaUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Ha ocurrido un error al enviar el formulario"))
        return super(AreaUpdateView, self).form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        context['accion'] = _('Editar')
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )


class ListaAreasView(ListView):
    """Devuelve una lista de areas ingresadas en el sistema."""
    model = Area
    template_name = 'organizacional/listar_areas.html'
    group_required = ['administrador sgd']


class DepartamentoCreateView(CreateView):
    """CreateView for AreaCreateView"""
    model = Departamento
    form_class = DepartamentoForm
    # fields = ['nombre', 'codigo']
    success_url = reverse_lazy('organizacional:crear_departamento')
    template_name = 'organizacional/crear_departamento.html'
    group_required = ['administrador sgd']

    def form_valid(self, form):
        messages.success(self.request, _("Se ha creado exitosamente el Departamento"))
        return super(DepartamentoCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Ha ocurrido un error al enviar el formulario"))
        return super(DepartamentoCreateView, self).form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        context['accion'] = _('Crear')
        # context['tipo'] = 'Area'
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )


class DepartamentoUpdateView(UpdateView):
    """UpdateView for DepartamentoUpdateView"""
    model = Departamento
    form_class = DepartamentoForm
    # success_url = reverse_lazy('organizacional:editar_Departamento')
    template_name = 'organizacional/crear_departamento.html'
    group_required = ['administrador sgd']

    def form_valid(self, form):
        messages.success(self.request, _("Se ha editado exitosamente el Área"))
        self.success_url = reverse_lazy('organizacional:editar_departamento', args=(form.instance.id, ))
        return super(DepartamentoUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Ha ocurrido un error al enviar el formulario"))
        return super(DepartamentoUpdateView, self).form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        context['accion'] = _('Editar')
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )


class ListaDepartamentosView(ListView):
    """Devuelve una lista de areas ingresadas en el sistema."""
    model = Departamento
    template_name = 'organizacional/listar_departamentos.html'
    group_required = ['administrador sgd']


@login_required
def crear_empleado(request):
    """
    Vista de creacion de empleados y sus usuarios en el sistema de gestion documental
    """

    if request.method == 'POST':
        form = EmpleadoForm(data=request.POST)

        if form.is_valid():
            empleado = form.save(commit=False)
            # get_or_create
            usuario, created = User.objects.get_or_create(
                email=form.cleaned_data['correo'], defaults={
                    'password': '123456', 'username': form.cleaned_data['cedula']
                }
            )
            # usuario.email = form.cleaned_data['correo']
            if created:
                usuario.set_password(form.cleaned_data['contrasena'])
                usuario.save()
            usuario.groups.add(form.cleaned_data['tipo_usuario'])
            empleado.usuario = usuario
            empleado.save()
            form.save_m2m()
            messages.success(request, _('Empleado creado exitosamente'))
        else:
            messages.error(request, _('Ha ocurrido un error al enviar el formulario'))

    else:
        form = EmpleadoForm()

    data = {'form': form}

    return render(request, 'organizacional/crear_empleado.html', data)


class ListaEmpleadosView(ListView):
    """Devuelve una lista de areas ingresadas en el sistema."""
    model = Empleado
    template_name = 'organizacional/listar_empleados.html'
    group_required = ['administrador sgd']
