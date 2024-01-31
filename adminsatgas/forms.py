from django import forms

KATEGORI_INSTANSI_CHOICES = [
    ('Faskes','Faskes'),
    ('Non-faskes','Non-faskes'),
]

INSTANSI_CHOICES = [
    ('rumah sakit sehat','Rumah Sakit Sehat'),
    ('rumah sakit melati','Rumah Sakit Melati'),
    ('rumah sakit juanda','Rumah Sakit Juanda'),
    ('pt sosru','PT Sosrui'),
    ('rumah sakit adi mulya','Rumah Sakit Adi Mulya'),
    ('rumah sakit pertemanan','Rumah Sakit Pertemanan'),
    ('rumah sakit sejahtera','Rumah Sakit Sejahtera'),
    ('pt unilevel','PT Unilevel'),
    ('pt cipto indonesia','PT Cipto Indonesia'),
    ('rumah sakit bpjs','Rumah Sakit BPJS'),
    ('rumah sakit jakarta','Rumah Sakit Jakarta'),
    ('rumah sakit pertama','Rumah Sakit Pertama'),
    ('pt jakarta raya','PT Jakarta Raya'),
    ('rumah sakit ui', 'Rumah Sakit UI'),
    ('rumah sakit umum negeri','Rumah Sakit Umum Negeri'),
    ('rumah sakit merdeka','Rumah Sakit Merdeka'),
    ('pt dua harimau','PT Dua Harimau'),
    ('pt bintang pratama','PT Bintang Pratama'),
    ('rsu fatmawati','RSU Fatmawati'),
    ('rs pusat pertamina','RS Pusat Pertamina'),
    ('puskesmas pondok indah','Puskesmas Pondok Indah'),
    ('puskesmas sakit tebet','Puskesmas Sakit Tebet'),
    ('puskesmas siaga raya','Puskesmas Siaga Raya'),
    ('klinik agung jakarta','Klinik Agung Jakarta'),
    ('klinik indah medika','Klinik Indah Medika'),
]

PENERIMA_CHOICES = [
    ('umum', 'Umum'),
    ('internal', 'Internal'),
]

LOKASI_VAKSIN_CHOICES = [
    ('rosemary hospital center', 'Rosemary Hospital Center'),
    ('memorial medical center', 'Memorial Medical Center'),
    ('pine rest comunity hospital', 'Pine Rest Comunity Hospital'),
    ('morningside medical center', 'Morningside Medical Center'),
    ('heartstone community hospital', 'Heartstone community hospital'),
    ('heartstone community hospital', 'Pearl River Clinic'),
    ('greengrass medical center', 'Greengrass Medical Center'),
    ('hot springs hospital center', 'Hot Springs Hospital Center'),
    ('fountain valley hospital', 'Fountain Valley Hospital'),
    ('lowland general hospital', 'Lowland General Hospital'),
]

VAKSIN_CHOICES = [
    ('sinovac', 'Sinovac'),
    ('astrazeneca', 'Astrazeneca'),
    ('sinopharm', 'Sinopharm'),
    ('moderna', 'Moderna'),
    ('pfizer', 'Pfizer'),
]

KATEGORI_TIPE_FASKES_CHOICES = [
    ('Rumah Sakit','Rumah Sakit'),
    ('Puskesmas','Puskesmas'),
    ('Klinik','Klinik'),
]

KATEGORI_STATUS_KEPEMILIKAN = [
    ('Swasta', 'Swasta'),
    ('Pemerintah', 'Pemerintah'),
]

class KategoriInstansi(forms.Form):
    kategoriInstansi = forms.CharField(label='Role', widget=forms.Select(choices=KATEGORI_INSTANSI_CHOICES))

class VerifikasiPenjadwalanBaruForm(forms.Form):
    namaInstansi = forms.CharField(label='Nama instansi', widget=forms.Select(choices=INSTANSI_CHOICES))
    tanggalDanWaktu = forms.DateField(widget=forms.DateTimeInput)
    kuota = forms.CharField(label='Kuota', widget=forms.TextInput(attrs={'class': 'form-control'}))
    penerima = forms.CharField(label='Penerima', widget=forms.Select(choices=PENERIMA_CHOICES))
    lokasiVaksin = forms.CharField(label='Penerima', widget=forms.Select(choices=LOKASI_VAKSIN_CHOICES))
    jumlahNakes = forms.CharField(label='Jumlah Tenaga Kesehatan', widget=forms.TextInput(attrs={'class': 'form-control'}))

class AturDistribusiForm(forms.Form):
    namaInstansi = forms.CharField(label='Nama instansi', widget=forms.Select(choices=INSTANSI_CHOICES))
    tanggalDanWaktu = forms.DateField(widget=forms.DateTimeInput)
    kuota = forms.CharField(label='Kuota', widget=forms.TextInput(attrs={'class': 'form-control'}))
    penerima = forms.CharField(label='Penerima', widget=forms.Select(choices=PENERIMA_CHOICES))
    lokasiVaksin = forms.CharField(label='Penerima', widget=forms.Select(choices=LOKASI_VAKSIN_CHOICES))
    jumlahNakes = forms.CharField(label='Jumlah Tenaga Kesehatan', widget=forms.TextInput(attrs={'class': 'form-control'}))
    diverifikasiOleh = forms.CharField(label='Diverifikasi oleh', widget=forms.TextInput(attrs={'class': 'form-control'}))
    tanggalDanWaktuDistribusi = forms.DateField(widget=forms.DateTimeInput)
    biayaDistribusi = forms.CharField(label='Biaya Distribusi', widget=forms.TextInput(attrs={'class': 'form-control'}))
    jenisVaksin = forms.CharField(label='Jenis Vaksin', widget=forms.Select(choices=VAKSIN_CHOICES))
    jumlahVaksin = forms.CharField(label='Jumlah Vaksin', widget=forms.TextInput(attrs={'class': 'form-control'}))

class UpdateDistribusiForm(forms.Form):
    kode = forms.CharField(label='Kode', widget=forms.Select(choices=INSTANSI_CHOICES))
    tanggalDistribusi = forms.DateField(widget=forms.DateTimeInput)
    biayaDistribusi = forms.CharField(label='Biaya Distribusi', widget=forms.TextInput(attrs={'class': 'form-control'}))
    jenisVaksin = forms.CharField(label='Jenis Vaksin', widget=forms.Select(choices=VAKSIN_CHOICES))
    jumlahVaksin = forms.CharField(label='Jumlah Vaksin', widget=forms.TextInput(attrs={'class': 'form-control'}))

class KategoriInstansiForm(forms.Form):
    kategoriInstansi = forms.CharField(label='Role', widget=forms.Select(choices=KATEGORI_INSTANSI_CHOICES))
    kategoriTipeFaskes = forms.CharField(label='Role', widget=forms.Select(choices=KATEGORI_TIPE_FASKES_CHOICES))
    kategoriStatusKepemilikan = forms.CharField(label='Role', widget=forms.Select(choices=KATEGORI_STATUS_KEPEMILIKAN))

class UpdateStatusTiket(forms.Form):
    kode = forms.CharField(label='Kode', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    nama_status = forms.CharField(label='Nama Status', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))

class UpdateInstansi(forms.Form):
    kode_instansi = forms.CharField(label='Kode Instansi', widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}))
    nama_instansi = forms.CharField(label='Nama Instansi', widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}))
    kategoriInstansi = forms.CharField(label='Role', widget=forms.Select(choices=KATEGORI_INSTANSI_CHOICES))
    kategoriTipeFaskes = forms.CharField(label='Role', widget=forms.Select(choices=KATEGORI_TIPE_FASKES_CHOICES))
    kategoriStatusKepemilikan = forms.CharField(label='Role', widget=forms.Select(choices=KATEGORI_STATUS_KEPEMILIKAN))

class TambahVaksinForm(forms.Form):
    kode = forms.CharField(label='Kode', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nama = forms.CharField(label='Nama Vaksin', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nama_produsen = forms.CharField(label='Produsen', widget=forms.TextInput(attrs={'class': 'form-control'}))
    no_edar = forms.CharField(label='No. Edar', widget=forms.TextInput(attrs={'class': 'form-control'}))
    stok = forms.CharField(label='Stok', widget=forms.TextInput(attrs={'class': 'form-control'}))
    freq_suntik = forms.CharField(label='Frekuensi', widget=forms.TextInput(attrs={'class': 'form-control'}))

class TambahStatusTiket(forms.Form):
    kode = forms.CharField(label='Kode', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nama_status = forms.CharField(label='Nama Status', widget=forms.TextInput(attrs={'class': 'form-control'}))
    