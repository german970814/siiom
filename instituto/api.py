from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, generics, status
from rest_framework.decorators import api_view

from . import models, serializers


# TODO: add support for waffle instituto
class CursoListAPIView(generics.ListAPIView):
    queryset = models.Curso.objects.all()
    serializer_class = serializers.CursoSerializer

    def get_queryset(self, *args, **kwargs):
        salon_id = self.kwargs.get('pk')
        return super().get_queryset(*args, **kwargs).filter(salon_id=salon_id)

    def get_serializer(self, *args, **kwargs):
        kwargs['expand'] = ['materia', ]
        return super().get_serializer(*args, **kwargs)


@api_view(['GET', 'POST'])
def curso_by_month(request, pk):
    if request.method == 'GET':
        salon = get_object_or_404(models.Salon, pk=pk)

        _serializer = serializers.CursoEventoSerializer(data=request.GET)
        if _serializer.is_valid():
            cursos = models.Curso.objects.filter(
                fecha_inicio__lte=_serializer.data['end'],
                fecha_fin__gte=_serializer.data['start'], salon=salon)
            serializer = serializers.CursoSerializer(cursos, many=True, expand=['materia', ])
            response = Response(serializer.data)
        else:
            response = Response(_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return response


@api_view(['GET', ])
def verifica_disponibilidad_curso(request, pk):
    salon = get_object_or_404(models.Salon, pk=pk)

    serializer = serializers.CursoEventoSerializer(data=request.GET)
    # dias = request.GET.getlist('dias[]')

    if serializer.is_valid():
        cursos = models.Curso.objects.filter(
            salon_id=salon.id, dia__overlap=serializer.data['dias'],
            fecha_inicio__lte=serializer.data['end'], fecha_fin__gte=serializer.data['start'],
            hora_inicio__lte=serializer.data['end_hour'], hora_fin__gte=serializer.data['start_hour']
        )
        response = Response({'valid': not cursos.exists()})
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return response
