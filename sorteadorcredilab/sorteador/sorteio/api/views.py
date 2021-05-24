from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import status, filters
from rest_framework.response import Response

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

