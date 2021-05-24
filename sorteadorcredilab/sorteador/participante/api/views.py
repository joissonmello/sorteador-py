from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from sorteadorcredilab.sorteador.models import Participante
from sorteadorcredilab.sorteador.participante.api.serializers import ParticipanteSerializer


class ParticipanteView(ModelViewSet):
    queryset = Participante.objects.filter(ativo=True).order_by('nome')
    serializer_class = ParticipanteSerializer
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ('id', 'nome')
    search_fields = ('id', 'nome')
