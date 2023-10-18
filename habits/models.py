from django.db import models
from config import settings


NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):

    class Frequency(models.TextChoices):
        daily = 'Daily'
        monday = 'Monday'
        tuesday = 'Tuesday'
        wednesday = 'Wednesday'
        thursday = 'Thursday'
        friday = 'Friday'
        saturday = 'Saturday'
        sunday = 'Sunday'

    place = models.CharField(max_length=100, verbose_name='место выполнения задачи')
    time = models.TimeField(default='12:00', verbose_name='время выполнения задачи')
    action = models.CharField(max_length=100, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    link_pleasant = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, verbose_name='связанная привычка')
    frequency = models.CharField(choices=Frequency.choices, default=Frequency.daily, verbose_name='периодичность')
    award = models.CharField(max_length=100, **NULLABLE, verbose_name='вознаграждение')
    duration = models.IntegerField(**NULLABLE, verbose_name='время выполнения')
    is_public = models.BooleanField(default=True, verbose_name='признак публичной привычки')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return {self.action}

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
