from django.shortcuts import render
from .models import Plant


def plant_list(request):
    plants = Plant.objects.all()
    return render(request, 'plants/plant_list.html', {'plants': plants})


from django.shortcuts import get_object_or_404, redirect
from .models import Plant, Fertilizer, FeedingSchedule
from django.utils import timezone
from datetime import timedelta
import plotly.express as px
import pandas as pd


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    fertilizers = Fertilizer.objects.all()
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
            current_date = start_date
            for i in range(8):
                dates.append(current_date)
                current_date = current_date + timedelta(days=plant.feeding_interval_days)

            dosages = [float(dosage_ml)] * 8

            df = pd.DataFrame({
                'Дата': dates,
                'Дозировка (мл)': dosages
            })

            fig = px.line(df, x='Дата', y='Дозировка (мл)',
                          title=f'График подкормок для {plant.name}',
                          markers=True)
            graph_html = fig.to_html(full_html=False)

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'fertilizers': fertilizers,
        'dosage_ml': dosage_ml,
        'graph_html': graph_html,
        'error': error,
    })