from django.shortcuts import render
from .models import Plant


def plant_list(request):
    """Страница со списком всех растений с поиском"""
    query = request.GET.get('q', '')
    if query:
        plants = Plant.objects.filter(name__iregex=query)
    else:
        plants = Plant.objects.all()
    return render(request, 'plants/plant_list.html', {
        'plants': plants,
        'query': query,
    })

from django.shortcuts import get_object_or_404, redirect
from .models import Plant, Fertilizer, FeedingSchedule
from django.utils import timezone
from datetime import timedelta
import plotly.express as px
import pandas as pd


def plant_detail(request, plant_id):
    """Страница с деталями растения и формой подбора удобрения"""
    plant = get_object_or_404(Plant, id=plant_id)
    fertilizers = Fertilizer.objects.all()

    recommended = None
    if plant.growth_phase == 'growth':
        recommended = fertilizers.filter(type='mineral').first()
    elif plant.growth_phase == 'flowering':
        recommended = fertilizers.filter(type='organic').first()
    else:
        recommended = fertilizers.filter(type='universal').first()

    schedule = None
    graph_html = None
    dosage_ml = None
    error = None

    if request.method == 'POST':
        fertilizer_id = request.POST.get('fertilizer')
        water_volume = request.POST.get('water_volume')

        if not water_volume:
            error = 'Введите объём воды'
        else:
            water_volume = float(water_volume)
            fertilizer = get_object_or_404(Fertilizer, id=fertilizer_id)

            dosage_ml = float(fertilizer.concentration_ml_per_liter) * water_volume

            start_date = timezone.now().date()
            dates = []
            dosages = []
            current_date = start_date
            current_dosage = float(dosage_ml)

            for i in range(8):
                dates.append(current_date)
                dosages.append(round(current_dosage, 1))
                current_date = current_date + timedelta(days=plant.feeding_interval_days)
                current_dosage = current_dosage * 1.05

            df = pd.DataFrame({
                'Дата': dates,
                'Дозировка (мл)': dosages
            })

            fig = px.bar(
                df,
                x='Дата',
                y='Дозировка (мл)',
                title=f'График подкормок: {plant.name}',
                text='Дозировка (мл)',
                color='Дозировка (мл)',
                color_continuous_scale='Greens'
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(
                xaxis_title='Дата подкормки',
                yaxis_title='Объём удобрения (мл)',
                title_font_size=18,
            )
            graph_html = fig.to_html(full_html=False)

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'fertilizers': fertilizers,
        'recommended': recommended,
        'dosage_ml': dosage_ml,
        'graph_html': graph_html,
        'error': error,
    })