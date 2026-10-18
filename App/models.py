from django.db import models
from django.contrib.auth.models import User


class Aula(models.Model):
    materia = models.CharField(max_length=100, verbose_name="Matéria")
    conteúdo = models.TextField(verbose_name="Conteúdo da Aula")
    data = models.DateField(verbose_name="Data da Aula")
    horario = models.TimeField(verbose_name="Horário da Aula")
    vagas = models.PositiveIntegerField(verbose_name="Número de Vagas")
    inscritos = models.ManyToManyField(User, related_name='aulas_inscritas', blank=True)


    def __str__(self):
        return f"{self.materia} - {self.data} às {self.horario}"



