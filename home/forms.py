from django import forms
from django.db import connection

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

ROLE_CHOICES = [
    ('admin satgas','Admin Satgas'),
    ('panitia penyelenggara','Panitia Penyelenggara'),
    ('warga','Warga'),
]

GENDER_CHOICES = [
    ('M','laki-laki'),
    ('F','perempuan'),
]

YESNO_CHOICES = [
    ('yes','yes'),
    ('no','no'),
]

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
    INSTANSI_CHOICES.append(tuple((psdf[i].get('kode') , psdf[i].get('kode'))))

class RegisterAdminSatgasForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    noHp = forms.CharField(label='No. Hp', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nomorPetugas = forms.CharField(label='Nomor Petugas', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nik = forms.CharField(label='NIK', widget=forms.TextInput(attrs={'class': 'form-control'}))
    namaPanjang = forms.CharField(label='Nama Panjang', widget=forms.TextInput(attrs={'class': 'form-control'}))
    jenisKelamin = forms.CharField(label='Role', widget=forms.Select(choices=GENDER_CHOICES))
    nomorBangunan = forms.CharField(label='Nomor Bangunan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    namajalan = forms.CharField(label='Nama Jalan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kelurahan = forms.CharField(label='Kelurahan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kecamatan = forms.CharField(label='Kecamatan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kotaAdministrasi = forms.CharField(label='Kota Administrasi', widget=forms.TextInput(attrs={'class': 'form-control'}))
    instansi = forms.CharField(label='Instansi', widget=forms.Select(choices=INSTANSI_CHOICES))
    
class RegisterPanitiaPenyelenggaraForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    noHp = forms.CharField(label='No. Hp', widget=forms.TextInput(attrs={'class': 'form-control'}))
    namaPanjang = forms.CharField(label='Nama Lengkap', widget=forms.TextInput(attrs={'class': 'form-control'}))
    isTenagaKesehatan = forms.ChoiceField(label='Tenaga Kesehatan', choices = YESNO_CHOICES, widget=forms.RadioSelect)
    nomorSTR = forms.CharField(label='Nomor STR', widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipePetugas = forms.CharField(label='Tipe Petugas', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nik = forms.CharField(label='NIK', widget=forms.TextInput(attrs={'class': 'form-control'}))
    jenisKelamin = forms.CharField(label='Role', widget=forms.Select(choices=GENDER_CHOICES))
    nomorBangunan = forms.CharField(label='Nomor Bangunan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    namajalan = forms.CharField(label='Nama Jalan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kelurahan = forms.CharField(label='Kelurahan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kecamatan = forms.CharField(label='Kecamatan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kotaAdministrasi = forms.CharField(label='Kota Administrasi', widget=forms.TextInput(attrs={'class': 'form-control'}))
    instansi = forms.CharField(label='Instansi', widget=forms.Select(choices=INSTANSI_CHOICES))
    
class RegisterWargaForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    noHp = forms.CharField(label='No. Hp', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nik = forms.CharField(label='NIK', widget=forms.TextInput(attrs={'class': 'form-control'}))
    namaPanjang = forms.CharField(label='Nama Lengkap', widget=forms.TextInput(attrs={'class': 'form-control'}))
    jenisKelamin = forms.CharField(label='Role', widget=forms.Select(choices=GENDER_CHOICES))
    nomorBangunan = forms.CharField(label='Nomor Bangunan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    namajalan = forms.CharField(label='Nama Jalan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kelurahan = forms.CharField(label='Kelurahan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kecamatan = forms.CharField(label='Kecamatan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    kotaAdministrasi = forms.CharField(label='Kota Administrasi', widget=forms.TextInput(attrs={'class': 'form-control'}))
    instansi = forms.CharField(label='Instansi', widget=forms.Select(choices=INSTANSI_CHOICES))