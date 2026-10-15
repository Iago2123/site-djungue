from django.db import models
from django.contrib.auth.models import User

class PacoteViagem(models.Model):
    cidade = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default="Brasil")
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    foto = models.ImageField(upload_to='viagens/')
    vagas_disponiveis = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.cidade} ({self.data_inicio} até {self.data_fim})"

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pacote = models.ForeignKey(PacoteViagem, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.pacote.cidade}"

class HistoricoClima(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cidade_buscada = models.CharField(max_length=100)
    data_pesquisa = models.DateTimeField(auto_now_add=True)
    temperatura = models.CharField(max_length=10)
    condicao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cidade_buscada} - {self.data_pesquisa.strftime('%d/%m/%Y')}"


# Create your models here.
