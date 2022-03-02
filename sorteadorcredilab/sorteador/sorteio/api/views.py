from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import status, filters
from rest_framework.response import Response
from django.db.models import Count

from sorteadorcredilab.sorteador.sorteio.api.serializers import SorteioSerializer
from sorteadorcredilab.sorteador.models import Sorteio


class SorteioView(ModelViewSet):
    queryset = Sorteio.objects.all().order_by('data')
    serializer_class = SorteioSerializer
    http_method_names = ['get', 'post']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('id', 'data')
    search_fields = ('id', 'data')

    @action(methods=['get'], detail=False, url_path='sorteios-da-semana')
    def sorteios_da_semana(self, request):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        sorteios = Sorteio.objects.filter(data__gt=data_inicio, data__lt=data_fim)

        return Response(SorteioSerializer(sorteios, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='ranking')
    def ranking(self, request):
        ano = request.query_params.get('ano')

        sorteios = Sorteio.objects.all()

        if ano:
            sorteios = Sorteio.objects.filter(data__year=ano)

        facilitadores = list(
            sorteios
            .values('facilitador', 'facilitador__nome', 'facilitador__avatar')
            .annotate(total=Count('id'))
            .order_by('-total')
            .values('facilitador', 'facilitador__nome', 'facilitador__avatar', 'total')
        )

        secretarios = list(
            sorteios
            .values('secretario', 'secretario__nome', 'secretario__avatar')
            .annotate(total=Count('id'))
            .order_by('-total')
            .values('secretario', 'secretario__nome', 'secretario__avatar', 'total')
        )

        return Response({
            'total_sorteios': sorteios.count(),
            'facilitadores': facilitadores,
            'secretarios': secretarios,
        }, status=status.HTTP_200_OK)

