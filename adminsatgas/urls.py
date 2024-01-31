from django.urls import path

from . import views

app_name = 'adminsatgas'

urlpatterns = [
    path('', views.profilAdminSatgas, name='profilAdminSatgas'),
    path('pembuatanTiket', views.pembuatanTiket, name='pembuatanTiket'),
    path('tambahVaksin', views.tambahVaksin, name='tambahVaksin'),
    path('masterStatus', views.masterStatus, name='masterStatus'),
    path('tambahInstansi', views.tambahInstansi, name='tambahInstansi'),
    path('verifikasiPenjadwalan', views.verifikasiPenjadwalan, name='verifikasiPenjadwalan'),
    path('detailPenjadwalanAdmin', views.detailPenjadwalanAdmin, name='detailPenjadwalanAdmin'),
    path('aturDistribusiForm', views.aturDistribusiForm, name='aturDistribusiForm'),
    path('detailDistribusi', views.detailDistribusi, name='detailDistribusi'),
    path('updateDistribusiForm', views.updateDistribusiForm, name='updateDistribusiForm'),
    path('dataDistribusi', views.dataDistribusi, name='dataDistribusi'),
    path('daftarVaksin', views.daftarVaksin, name='daftarVaksin'),
    path('updateStokVaksin/(?P<kode>[0-9]$)/', views.updateStokVaksin, name='updateStokVaksin'),
    path('daftarPengajuanVaksin', views.daftarPengajuanVaksin, name='daftarPengajuanVaksin'),
    path('updateStatusTiket/(?P<kode>[0-9]$)', views.updateStatusTiket, name='updateStatusTiket'),
    path('/hapusStatusTiket/(?P<kode>[0-9]$)', views.hapusStatusTiket, name='hapusStatusTiket'),
    path('/hapusInstansi/(?P<kode>[0-9]$)', views.hapusInstansi, name='hapusInstansi'),
    path('masterInstansi', views.masterInstansi, name='masterInstansi'),
    path('detailInstansiFaskes/<kode>', views.detailInstansiFaskes, name='detailInstansiFaskes'),
    path('detailInstansiNonFaskes/<kode>', views.detailInstansiNonFaskes, name='detailInstansiNonFaskes'),
    path('updateInstansiFaskes', views.updateInstansiFaskes, name='updateInstansiFaskes'),
    path('updateInstansiNonFaskes', views.updateInstansiNonFaskes, name='updateInstansiNonFaskes'),
    path('tambahStatus/(?P<kode>[0-9]$)', views.tambahStatus, name='tambahStatus'),
]
