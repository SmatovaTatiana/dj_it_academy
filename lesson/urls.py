from django.urls import path
from . import views

app_name = 'lesson'
urlpatterns = [
    path('', views.all_materials, name='all_material'),
]
