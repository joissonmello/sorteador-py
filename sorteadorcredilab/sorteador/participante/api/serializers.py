from sorteadorcredilab.sorteador.models import Participante
from rest_framework import serializers


class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'