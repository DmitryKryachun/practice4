from pyexpat import model
import django
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Grain(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва культури')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Культура'
        verbose_name_plural = 'Культури'

class Bunker(models.Model):
    name = models.CharField(max_length=30, verbose_name='Назва бункеру')
    max_qty = models.PositiveIntegerField(default=10000, verbose_name='Вмісткість (кг)')
    qty = models.PositiveIntegerField(default=0, verbose_name='Займано в бункері')
    transactions = models.ManyToManyField('Transaction', blank=True, related_name='related_bunker', verbose_name='Транзакції')
    grain_type = models.ForeignKey(Grain, verbose_name='Вид культури', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бункер'
        verbose_name_plural = 'Бункери'


class Transaction(models.Model):
    title = models.CharField(max_length=100, verbose_name='Опис транзакції')
    qty = models.IntegerField(default=1000, verbose_name='Кількість (кг)')
    bunker = models.ForeignKey(Bunker, verbose_name='Бункер', on_delete=models.CASCADE, related_name='related_transaction')
    transaction_date = models.DateField(verbose_name='Дата транзакції', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Транзакція'
        verbose_name_plural = 'Транзакції'

