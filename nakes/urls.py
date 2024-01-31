from django.urls import path

from . import views

app_name = 'nakes'

urlpatterns = [
    path('listTiket', views.listTiket, name='listTiket'),
    path('detailTiket/(?P<no_tiket>[0-9]$)/', views.detailTiket, name='detailTiket'),
    path('updateTiket/(?P<no_tiket>[0-9]$)/', views.updateTiket, name='updateTiket'),
    path('profilNakes', views.profilNakes, name='profilNakes'),
]