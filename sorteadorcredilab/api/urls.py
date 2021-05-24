from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sorteadorcredilab.sorteador.participante.api.views import ParticipanteView
from sorteadorcredilab.sorteador.sorteio.api.views import SorteioView


app_name = 'api'

router = DefaultRouter()
router.register('participante', ParticipanteView)
router.register('sorteio', SorteioView)

urlpatterns = [
    path('', include(router.urls)),
]