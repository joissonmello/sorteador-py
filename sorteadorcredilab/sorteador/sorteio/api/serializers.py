from sorteadorcredilab.sorteador.models import Sorteio
from rest_framework import serializers


class SorteioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sorteio
        fields = '__all__'