from django import forms
from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

INSTANSI_CHOICES = []
query = """
select * from instansi;
"""
cursor = connection.cursor()
cursor.execute("SET search_path TO sivax;")

cursor.execute(query)
psdf = dictfetchall(cursor)

for i in range (len(psdf)):
    INSTANSI_CHOICES.append(tuple((psdf[i].get('nama_instansi') , psdf[i].get('nama_instansi'))))

PENERIMA_CHOICES = [
    ('umum', 'Umum'),
    ('internal', 'Internal'),
]

LOKASI_VAKSIN_CHOICES = []

query2 = """
select * from lokasi_vaksin;
"""
cursor = connection.cursor()
cursor.execute("SET search_path TO sivax;")

cursor.execute(query2)
lv = dictfetchall(cursor)

for i in range (len(lv)):
    LOKASI_VAKSIN_CHOICES.append(tuple((lv[i].get('nama') , lv[i].get('nama'))))

class TambahPenjadwalanForm(forms.Form):
    namaInstansi = forms.CharField(label='Nama instansi', widget=forms.Select(choices=INSTANSI_CHOICES))
    tanggalDanWaktu = forms.CharField(label='Tanggal dan Waktu', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kuota = forms.CharField(label='Kuota', widget=forms.TextInput(attrs={'class': 'form-control'}))
    penerima = forms.CharField(label='Penerima', widget=forms.Select(choices=PENERIMA_CHOICES))
    lokasiVaksin = forms.CharField(label='Penerima', widget=forms.Select(choices=LOKASI_VAKSIN_CHOICES))

class UpdatePenjadwalanForm(forms.Form):
    namaInstansi = forms.CharField(label='Nama instansi', widget=forms.Select(choices=INSTANSI_CHOICES))
    tanggalDanWaktu = forms.DateField(widget=forms.DateTimeInput)
    kuota = forms.CharField(label='Kuota', widget=forms.TextInput(attrs={'class': 'form-control'}))
    penerima = forms.CharField(label='Penerima', widget=forms.Select(choices=PENERIMA_CHOICES))
    lokasiVaksin = forms.CharField(label='Penerima', widget=forms.Select(choices=LOKASI_VAKSIN_CHOICES))