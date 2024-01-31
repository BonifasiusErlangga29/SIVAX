from django.urls import path

from . import views

app_name = 'panitiapenyelenggara'

urlpatterns = [
    path('', views.profilPanitiaPenyelenggara, name='profilPanitiaPenyelenggara'),
    path('tambahPenjadwalanBaru', views.tambahPenjadwalanBaru, name='tambahPenjadwalanBaru'),
    path('daftarPenjadwalanVaksin', views.daftarPenjadwalanVaksin, name='daftarPenjadwalanVaksin'),
    path('detailPenjadwalan/(?P<nama_instansi>[0-9]$)/(?P<kode_distribusi>[0-9]$)', views.detailPenjadwalan, name='detailPenjadwalan'),
    path('updatePenjadwalan', views.updatePenjadwalan, name='updatePenjadwalan'),
]