from django.contrib import admin
from .models import Plant, Fertilizer, FeedingSchedule


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'latin_name', 'growth_phase', 'feeding_interval_days')
    search_fields = ('name', 'latin_name')
    list_filter = ('growth_phase',)


@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'npk_ratio', 'concentration_ml_per_liter')
    search_fields = ('name',)


@admin.register(FeedingSchedule)
class FeedingScheduleAdmin(admin.ModelAdmin):
    list_display = ('plant', 'fertilizer', 'start_date', 'dosage_ml', 'next_feeding_date')
    search_fields = ('plant__name', 'fertilizer__name')
    list_filter = ('plant__growth_phase',)