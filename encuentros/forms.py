
# Django
from django import forms

# Apps
from .models import Encuentro, Encontrista
from grupos.models import Grupo, Red
from miembros.models import Miembro
# from reportes.views import listaGruposDescendientes


class CrearEncuentroForm(forms.ModelForm):
    """
    Formulario para crear encuentros
    """

    class Meta:
        model = Encuentro
        exclude = ('dificultades', 'estado')

    error_css_class = 'has-error'
    red = forms.ModelChoiceField(queryset=Red.objects.all())

    def __init__(self, *args, **kwargs):
        super(CrearEncuentroForm, self).__init__(*args, **kwargs)
        self.fields['grupos'].queryset = Grupo.objects.prefetch_related('lideres').all()
        self.fields['coordinador'].queryset = Miembro.objects.none()
        self.fields['tesorero'].queryset = Miembro.objects.none()
        for x in self.fields:
            self.fields[x].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_inicial'].widget.attrs.update({'data-mask': '00/00/00 00:00'})
        self.fields['fecha_final'].widget.attrs.update({'data-mask': '00/00/00'})
        self.fields['coordinador'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['red'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['tesorero'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['observaciones'].widget.attrs.update({'rows': '5'})
        self.fields['grupos'].widget.attrs.update(
            {
                'class': 'selectpicker',
                'data-live-search': 'true',
                'data-actions-box': 'true',
                'multiple data-selected-text-format': 'count'
            }
        )

        if self.is_bound:
            try:
                tesorero = self.data.get('tesorero', None)
                coordinador = self.data.get('coordinador', None)
                queryset_tesorero = Miembro.objects.filter(id=tesorero)
                queryset_coordinador = Miembro.objects.filter(id=coordinador)
            except:
                queryset_tesorero = Miembro.objects.none()
                queryset_coordinador = Miembro.objects.none()
            self.fields['tesorero'].queryset = queryset_tesorero
            self.fields['coordinador'].queryset = queryset_coordinador


class NuevoEncontristaForm(forms.ModelForm):
    """
    Formulario Para la Creacion de Encontristas
    """
    error_css_class = 'has-error'

    class Meta:
        model = Encontrista
        exclude = ('encuentro', )

    def __init__(self, encuentro=None, *args, **kwargs):
        super(NuevoEncontristaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        if encuentro:
            self.fields['grupo'].queryset = Grupo.objects.none()
        else:
            self.fields['grupo'].queryset = Grupo.objects.filter(id=self.instance.grupo.id)
        self.fields['grupo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['genero'].widget.attrs.update({'class': 'selectpicker'})

        if self.is_bound:
            try:
                grupo = self.data.get('grupo', None)
                queryset = Grupo.objects.filter(id=grupo)
            except:
                queryset = Grupo.objects.none()
            self.fields['grupo'].queryset = queryset


class EditarEncuentroForm(CrearEncuentroForm):
    def __init__(self, *args, **kwargs):
        super(EditarEncuentroForm, self).__init__(*args, **kwargs)
        self.fields['coordinador'].widget.attrs.update({'readonly': ''})
        self.fields['tesorero'].widget.attrs.update({'readonly': ''})

        if not self.is_bound:
            if self.instance:
                if any(self.instance.grupos.all()):
                    self.fields['red'].initial = self.instance.grupos.first().red

                self.fields['coordinador'].queryset = Miembro.objects.filter(id=self.instance.coordinador.id)
                self.fields['coordinador'].initial = self.instance.coordinador

                self.fields['tesorero'].queryset = Miembro.objects.filter(id=self.instance.tesorero.id)
                self.fields['tesorero'].initial = self.instance.tesorero
