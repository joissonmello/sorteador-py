from django.db import models

# Create your models here.

class Participante(models.Model):
    nome = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    nome_slack = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Sorteio(models.Model):
    data = models.DateField()
    facilitador = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name="facilitador")
    secretario = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name="secretario")
    notificado = models.BooleanField(default=False)