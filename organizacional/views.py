# Django Package
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db.models.functions import Lower

# Third Apps
from braces.views import LoginRequiredMixin, GroupRequiredMixin

# Locale Apps
# from gestion_documental.models import Documento
from .models import Area, Departamento, Empleado
from .forms import AreaForm, DepartamentoForm, EmpleadoForm, FormularioEditarEmpleado, NuevoEmpleadoForm

# Python Package
import json


@login_required
@csrf_exempt
def areas_departamento_json(request):
    """
    Vista que devuelve una lista de areas a partir de un departamento en formato json
    """

    if request.method == 'POST':
        try:
            departamento = get_object_or_404(Departamento, pk=request.POST['id_departamento'])
            areas = Area.objects.filter(departamento__id=departamento.id)
        except:
            areas = Area.objects.none()

        response = [{'id': area.id, 'area': area.nombre} for area in areas]

        return HttpResponse(json.dumps(response), content_type='application/json')


class AreaCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """CreateView for AreaCreateView"""
    model = Area
    form_class = AreaForm
    # fields = ['nombre', 'codigo']
    success_url = reverse_lazy('organizacional:crear_area')
    template_name = 'organizacional/crear_area.html'
    group_required = ['Administrador SGD']

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


class AreaUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """UpdateView for AreaUpdateView"""
    model = Area
    form_class = AreaForm
    # success_url = reverse_lazy('organizacional:editar_area')
    template_name = 'organizacional/crear_area.html'
    group_required = ['Administrador SGD']

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


class ListaAreasView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """Devuelve una lista de areas ingresadas en el sistema."""
    model = Area
    template_name = 'organizacional/listar_areas.html'
    group_required = ['Administrador SGD']


class DepartamentoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """CreateView for AreaCreateView"""
    model = Departamento
    form_class = DepartamentoForm
    # fields = ['nombre', 'codigo']
    success_url = reverse_lazy('organizacional:crear_departamento')
    template_name = 'organizacional/crear_departamento.html'
    group_required = ['Administrador SGD']

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


class DepartamentoUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """UpdateView for DepartamentoUpdateView"""
    model = Departamento
    form_class = DepartamentoForm
    # success_url = reverse_lazy('organizacional:editar_Departamento')
    template_name = 'organizacional/crear_departamento.html'
    group_required = ['Administrador SGD']

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


class ListaDepartamentosView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """Devuelve una lista de areas ingresadas en el sistema."""
    model = Departamento
    template_name = 'organizacional/listar_departamentos.html'
    group_required = ['Administrador SGD']


@login_required
@permission_required('organizacional.es_administrador_sgd')
def crear_empleado(request):
    """
    Vista de creacion de empleados y sus usuarios en el sistema de gestion documental
    """

    VERBO = _('Crear')

    if request.method == 'POST':
        form = EmpleadoForm(data=request.POST)

        if form.is_valid():
            empleado = form.save(commit=False)
            # se intenta buscar o crear el usuario
            usuario, created = User.objects.get_or_create(
                email=form.cleaned_data['correo'], defaults={
                    'password': '123456', 'username': form.cleaned_data['cedula']
                }
            )
            # si fue creado, le asigna la contraseña del formulario
            if created:
                usuario.set_password(form.cleaned_data['contrasena'])
                usuario.save()
            else:
                # si no fue creado, quiere decir que algun miembro puede tener ese usuario
                miembro = usuario.miembro_set.first()  # Si no tiene puede devolver None
                if miembro:
                    # de tener un miembro se reemplazan los campos por los del miembro
                    empleado.primer_nombre = miembro.nombre
                    empleado.cedula = miembro.cedula
                    empleado.primer_apellido = miembro.primerApellido
                    if miembro.segundoApellido:
                        empleado.segundo_apellido = miembro.segundoApellido
            # se agrega el tipo de usuario
            if 'tipo_usuario' in form.cleaned_data and form.cleaned_data['tipo_usuario'] is not None:
                usuario.groups.add(form.cleaned_data['tipo_usuario'])
            empleado.usuario = usuario
            # se crea el empleado
            empleado.save()
            form.save_m2m()

            if empleado.jefe_departamento is True:
                for area in form.cleaned_data['departamento'].areas.all():
                    if area not in empleado.areas.all():
                        empleado.areas.add(area)

            messages.success(request, _('Empleado creado exitosamente'))
            return redirect(reverse('organizacional:crear_empleado'))
        else:
            messages.error(request, _('Ha ocurrido un error al enviar el formulario'))

    else:
        form = EmpleadoForm()

    data = {'form': form, 'VERBO': VERBO}

    return render(request, 'organizacional/crear_empleado.html', data)


@login_required
@permission_required('organizacional.es_administrador_sgd')
def editar_empleado(request, id_empleado):
    """
    Edita los empleados
    """
    VERBO = 'Editar'
    _accept = ['administrador sgd', 'digitador', 'presidente']
    empleado = get_object_or_404(Empleado, pk=id_empleado)
    try:
        grupo = empleado.usuario.groups.annotate(nombre=Lower('name')).filter(nombre__in=_accept)[0]
    except IndexError:
        grupo = None

    if request.method == 'POST':
        form = FormularioEditarEmpleado(data=request.POST, instance=empleado)
        if form.is_valid():
            empleado = form.save(commit=False)
            if 'contrasena' in form.cleaned_data and form.cleaned_data['contrasena'] != '':
                empleado.usuario.set_password(form.cleaned_data['contrasena'])
            if form.cleaned_data['tipo_usuario'] is not None and form.cleaned_data['tipo_usuario'] != grupo:
                empleado.usuario.groups.remove(grupo)
                empleado.usuario.groups.add(form.cleaned_data['tipo_usuario'])
            empleado.usuario.save()
            empleado.save()
            form.save_m2m()

            if empleado.jefe_departamento is True:
                for area in form.cleaned_data['departamento'].areas.all():
                    if area not in empleado.areas.all():
                        empleado.areas.add(area)
            messages.success(request, _('Se ha editado exitosamente'))
            return redirect(reverse('organizacional:editar_empleado', args=(id_empleado, )))
        else:
            messages.error(request, _('Ha ocurrido un error al enviar el formulario'))
    else:
        initial = {
            'correo': empleado.usuario.email,
            'tipo_usuario': grupo,
            'areas': empleado.areas.all()
        }
        form = FormularioEditarEmpleado(instance=empleado, initial=initial)

    data = {'VERBO': VERBO, 'form': form}

    return render(request, 'organizacional/crear_empleado.html', data)


class ListaEmpleadosView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """Devuelve una lista de areas ingresadas en el sistema."""
    model = Empleado
    template_name = 'organizacional/listar_empleados.html'
    group_required = ['Administrador SGD']

# --------------------------------------------------------


@login_required
@permission_required('organizacional.es_administrador_sgd', raise_exception=True)
def crear_empleado2(request):
    """
    Permite a un administrador crear empleados para una iglesia.
    """

    VERBO = _('Crear')
    if request.method == 'POST':
        form = NuevoEmpleadoForm(data=request.POST)
    else:
        form = NuevoEmpleadoForm()

    return render(request, 'organizacional/empleado_form.html', {'form': form, 'VERBO': VERBO})
