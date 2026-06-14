from django.contrib import admin
from django.urls import path
from plants.views import plant_list, plant_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', plant_list, name='plant_list'),
    path('plant/<int:plant_id>/', plant_detail, name='plant_detail'),
]
