from django.shortcuts import render,redirect
from django.http import HttpResponse, request
from django.db import connection
from .forms import *
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def profilPanitiaPenyelenggara(request):
    email = request.session.get('email')
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to sivax;")
        cursor.execute("SELECT * from panitia_penyelenggara WHERE email = '{}';".format(email))
        data = cursor.fetchone()
        print(data)
        args = {
            'data' : data,
        }
        return render(request, 'panitiapenyelenggara/profilPanitiaPenyelenggara.html', args)

def tambahPenjadwalanBaru(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            form = TambahPenjadwalanForm(request.POST)
            namaInstansi = request.POST.get('namaInstansi')
            tanggalDanWaktu = request.POST.get('tanggalDanWaktu')
            kuota = request.POST.get('kuota')
            penerima = request.POST.get('penerima')
            lokasiVaksin = request.POST.get('lokasiVaksin')

            getKodeInstansi = """
            select kode from instansi
            where nama_instansi = '{}';
            """.format(namaInstansi)
            cursor = connection.cursor()
            cursor.execute("SET search_path to sivax;")
            cursor.execute(getKodeInstansi)
            ki = dictfetchall(cursor)
            kodeInstansi = ki[0].get('kode')

            getKodeLokasi = """
            select kode from lokasi_vaksin
            where nama = '{}';
            """.format(lokasiVaksin)
            cursor = connection.cursor()
            cursor.execute("SET search_path to sivax;")
            cursor.execute(getKodeLokasi)
            lv = dictfetchall(cursor)
            kodeLokasi = lv[0].get('kode')
            print(kodeInstansi,tanggalDanWaktu,kuota,penerima,kodeLokasi)
            
            if form.is_valid():  
                cursor = connection.cursor()
                cursor.execute("SET search_path to sivax;")
                cursor.execute("INSERT INTO penjadwalan(kode_instansi, tanggal_waktu, jumlah, kategori_penerima, status, jumlah_nakes, kode_lokasi, email_admin)"
                                "VALUES ('{}', '{}', '{}', '{}', 'pengajuan dikirim', 0, '{}', 'Tallie.Pepperrall@gmail.com');".format(kodeInstansi, tanggalDanWaktu, kuota, penerima, kodeLokasi))
            
                return redirect('panitiapenyelenggara:daftarPenjadwalanVaksin')

        elif request.method == 'GET':
            form = TambahPenjadwalanForm()
        args = {
            'form' : form,
        }        
        return render(request, "panitiapenyelenggara/tambahPenjadwalan.html", {'form': form})

def daftarPenjadwalanVaksin(request):
    # instansi = request.session.get("instansi")
    query = """
    select i.nama_instansi, p.tanggal_waktu, p.jumlah, p.status, p.kode_distribusi
    from instansi i, penjadwalan p
    where i.kode = p.kode_instansi;
    """
    cursor = connection.cursor()
    cursor.execute("SET search_path TO sivax;")
    cursor.execute(query)

    p = dictfetchall(cursor)

    return render(request, "panitiapenyelenggara/daftarPenjadwalanVaksin.html", {'p':p})

def detailPenjadwalan(request, nama_instansi, kode_distribusi):
    getKode = """
    select kode from instansi where nama_instansi = '{}'
    """.format(nama_instansi)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO sivax;")
    cursor.execute(getKode)
    gk = dictfetchall(cursor)
    kodeInstansi = gk[0].get('kode')

    query = """
    select i.nama_instansi, p.tanggal_waktu, p.jumlah, p.kategori_penerima, l.nama, p.status, p.jumlah_nakes, p.email_admin
    from instansi i, penjadwalan p, lokasi_vaksin l
    where i.kode = p.kode_instansi and l.kode = p.kode_lokasi and p.kode_instansi = '{}';
    """.format(kodeInstansi)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO sivax;")
    cursor.execute(query)
    p = dictfetchall(cursor)

    if kode_distribusi != None :
        query2 = """
        select d.kode, d.tanggal, d.biaya, v.nama, p.jumlah
        from distribusi d,vaksin v, penjadwalan p
        where d.kode_vaksin = v.kode and p.kode_distribusi = d.kode and
        d.kode = '{}';
        """.format(kode_distribusi)
        cursor = connection.cursor()
        cursor.execute("SET search_path TO sivax;")
        cursor.execute(query2)
        d = dictfetchall(cursor)
        print(d)

        args = {
        'nama_instansi' : p[0].get('nama_instansi'),
        'tanggal_waktu' : p[0].get('tanggal_waktu'),
        'kuota' : p[0].get('kuota'),
        'kategori_penerima' : p[0].get('kategori_penerima'),
        'nama_lokasi' : p[0].get('nama'),
        'status_penerima': p[0].get('status'),
        'jumlah_nakes': p[0].get('jumlah_nakes'),
        'email_admin': p[0].get('email_admin'),
        'kode' : d[0].get('kode'),
        'tanggal' : d[0].get('tanggal'),
        'biaya' : d[0].get('biaya'),
        'nama' : d[0].get('nama'),
        'jumlah_vaksin' : p[0].get('kuota'),
        'kode_distribusi' : kode_distribusi
        }
        return render(request, "panitiapenyelenggara/detailPenjadwalan.html", args)

# ...
        
    args = {
        'nama_instansi' : p[0].get('nama_instansi'),
        'tanggal_waktu' : p[0].get('tanggal_waktu'),
        'kuota' : p[0].get('kuota'),
        'kategori_penerima' : p[0].get('kategori_penerima'),
        'nama_lokasi' : p[0].get('nama'),
        'status_penerima': p[0].get('status'),
        'jumlah_nakes': p[0].get('jumlah_nakes'),
        'email_admin': p[0].get('email_admin'),
        'kode_distribusi' : kode_distribusi
    }

    return render(request, "panitiapenyelenggara/detailPenjadwalan.html", args)

def updatePenjadwalan(request):
    form = UpdatePenjadwalanForm()
    return render(request, "panitiapenyelenggara/updatePenjadwalan.html", {'form': form})

def tambahPenjadwalan(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            nama_instansi = request.POST.get('kode')
            nama = request.POST.get('nama')
            nama_produsen = request.POST.get('nama_produsen')
            no_edar = request.POST.get('no_edar')
            stok = request.POST.get('stok')
            freq_suntik = request.POST.get('freq_suntik')
            


            try:
                #INSERT INTO VAKSIN
                cursor.execute("SET search_path TO sivax;")
                cursor.execute("INSERT INTO VAKSIN(kode, nama, nama_produsen, no_edar,freq_suntik, stok)"
                                "VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(kode, nama, nama_produsen, no_edar,freq_suntik, stok))

                
            except Exception as e:
                query = """
                SELECT *
                FROM vaksin where kode = '{}';   
                """.format(kode)

                print(e)
                cursor = connection.cursor()
                cursor.execute("SET search_path TO sivax;")
                cursor.execute(query)

                psdf = dictfetchall(cursor)
                if (len(psdf)!=0):
                    messages.error(request, 'Vaksin sudah pernah terdaftar!')
                else:
                    messages.error(request, 'Vaksin gagal ditambahkan, Coba Lagi!')
                return redirect('adminsatgas:tambahVaksin')

            return redirect('adminsatgas:daftarVaksin')

    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query2 = f"""
            select kode
            from vaksin
        """