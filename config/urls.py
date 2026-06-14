from django.contrib import admin
from django.urls import path
from plants.views import plant_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', plant_list, name='plant_list'),
]
