from django.urls import path

from . import views

app_name = 'pengguna'

urlpatterns = [
    path('detailJadwalTiket/<kode_instansi>/<tanggal_waktu>', views.detailJadwalTiket, name='jadwalListTiket'),
    path('detailJadwalVaksin/<kode_instansi>/<tanggal_waktu>', views.detailJadwalVaksin, name='detailJadwalVaksin'),
    path('detailKartuVaksin/(?P<no_sertifikat>[0-9]$)/', views.detailKartuVaksin, name='detailKartuVaksin'),
    path('detailKartuVaksin/<no_sertifikat>/download', views.downloadKartuVaksin, name='downloadKartuVaksin'),
    path('jadwalVaksin', views.jadwalVaksin, name='jadwalVaksin'),
    path('tiketSaya', views.tiketSaya, name='tiketSaya'),
    path('listKartuVaksin', views.listKartuVaksin, name='listKartuVaksin'),
    path('daftarVaksin', views.daftarVaksin, name='daftarVaksin'),
    path('tambahTiket/<kode_instansi>/<tanggal_waktu>/<no_tiket>', views.tambahTiket, name='tambahTiket'),
]