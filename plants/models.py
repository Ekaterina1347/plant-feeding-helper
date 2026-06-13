from django.db import models


class Plant(models.Model):
    PHASE_CHOICES = [
        ('growth', 'Рост'),
        ('flowering', 'Цветение'),
        ('rest', 'Покой'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    latin_name = models.CharField(max_length=100, blank=True, verbose_name='Латинское название')
    description = models.TextField(blank=True, verbose_name='Описание')
    growth_phase = models.CharField(
        max_length=20,
        choices=PHASE_CHOICES,
        default='growth',
        verbose_name='Фаза роста'
    )
    feeding_interval_days = models.PositiveIntegerField(
        default=14,
        verbose_name='Подкормка раз в N дней'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Растение'
        verbose_name_plural = 'Растения'


class Fertilizer(models.Model):
    TYPE_CHOICES = [
        ('mineral', 'Минеральное'),
        ('organic', 'Органическое'),
        ('universal', 'Универсальное'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='universal',
        verbose_name='Тип удобрения'
    )
    npk_ratio = models.CharField(
        max_length=20,
        verbose_name='Состав NPK',
        help_text='Например: 10-10-10'
    )
    concentration_ml_per_liter = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Концентрация (мл на 1 литр воды)'
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name} ({self.npk_ratio})'

    class Meta:
        verbose_name = 'Удобрение'
        verbose_name_plural = 'Удобрения'


class FeedingSchedule(models.Model):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        verbose_name='Растение'
    )
    fertilizer = models.ForeignKey(
        Fertilizer,
        on_delete=models.CASCADE,
        verbose_name='Удобрение'
    )
    start_date = models.DateField(verbose_name='Дата начала')
    dosage_ml = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Дозировка (мл)'
    )
    next_feeding_date = models.DateField(verbose_name='Следующая подкормка')

    def __str__(self):
        return f'{self.plant.name} — {self.fertilizer.name}'

    class Meta:
        verbose_name = 'График подкормки'
        verbose_name_plural = 'Графики подкормок'
