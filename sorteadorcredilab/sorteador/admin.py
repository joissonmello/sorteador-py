from sorteadorcredilab.sorteador.models import Participante, Sorteio
from django.contrib import admin

# Register your models here.

class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'avatar', 'nome_slack')

class SorteioAdmin(admin.ModelAdmin):
    list_display = ('id', 'data')


admin.site.register(Participante, ParticipanteAdmin)
admin.site.register(Sorteio, SorteioAdmin)