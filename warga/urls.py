from django.urls import path

from . import views

app_name = 'warga'

urlpatterns = [
    path('', views.profilWarga, name='profilWarga'),
]