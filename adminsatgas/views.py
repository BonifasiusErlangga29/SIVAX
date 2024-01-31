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


def profilAdminSatgas(request):
    email = request.session.get('email')
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to sivax;")
        cursor.execute("SELECT * FROM ADMIN_SATGAS WHERE email = '{}';".format(email))
        data = cursor.fetchone()
        print(data)
        args = {
            'data' : data,
        }
        return render(request, 'adminsatgas/profilAdminSatgas.html', args)


def pembuatanTiket(request):
    return render(request, 'adminsatgas/pembuatanTiket.html')

def tambahVaksin(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            kode = request.POST.get('kode')
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

        cursor.execute(query2)
        data2 = dictfetchall(cursor)

        code = int(data2[-1]['kode'][3:]) + 1

        response = {
            'kode': "vcn"+str(code),
        }
        return render(request, 'adminsatgas/tambahVaksin.html',response)

def masterStatus(request):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to sivax;")
        query = """
            SELECT kode, nama_status FROM STATUS_TIKET;
        """
        cursor.execute(query)
        data = dictfetchall(cursor)
       
        response = {
            'datas' : data,
        }
    return render(request, 'adminsatgas/masterStatus.html', response)

def tambahInstansi(request):
    return render(request, 'adminsatgas/tambahInstansi.html')

def verifikasiPenjadwalan(request):
    form = VerifikasiPenjadwalanBaruForm()
    return render(request, "adminsatgas/verifikasiPenjadwalan.html", {'form': form})

def detailPenjadwalanAdmin(request):
    return render(request, "adminsatgas/detailPenjadwalanAdmin.html")

def aturDistribusiForm(request):
    form = AturDistribusiForm()
    return render(request, "adminsatgas/aturDistribusiForm.html", {'form': form})

def detailDistribusi(request):
    return render(request, "adminsatgas/detailDistribusi.html")

def updateDistribusiForm(request):
    form = UpdateDistribusiForm()
    return render(request, "adminsatgas/updateDistribusiForm.html", {'form': form})

def dataDistribusi(request):
    query = """
    select d.kode, d.tanggal, d.biaya, v.nama, d.jumlah_vaksin
    from distribusi d, vaksin v where d.kode_vaksin = v.kode;
    """
    cursor = connection.cursor()
    cursor.execute("SET search_path TO sivax;")
    cursor.execute(query)

    disb = dictfetchall(cursor)
    return render(request, "adminsatgas/dataDistribusi.html", {'disb' : disb})

def updateStokVaksin(request, kode):
    query = """
    select email_pegawai, tgl_waktu, jumlah_update
    from update_stok where kode_vaksin = '{}';
    """.format(kode)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO sivax;")
    cursor.execute(query)

    vaks = dictfetchall(cursor)

    return render(request, "adminsatgas/updateStokVaksin.html", {'vaks': vaks})

def daftarPengajuanVaksin(request):
    query = """
    select i.nama_instansi, p.tanggal_waktu, p.jumlah, p.status, p.kode_distribusi
    from instansi i, penjadwalan p
    where i.kode = p.kode_instansi;
    """
    cursor = connection.cursor()
    cursor.execute("SET search_path TO sivax;")
    cursor.execute(query)

    daftarPenjadwalan = dictfetchall(cursor)

    return render(request, "adminsatgas/daftarPengajuanVaksin.html")
    # form = KategoriInstansiForm()
    # return render(request, "panitiapenyelenggara/daftarPenjadwalanVaksin.html")
    # return render(request, 'adminsatgas/tambahInstansi.html', {'form': form})

def updateStatusTiket(request, kode):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            form = UpdateStatusTiket(request.POST)
            if form.is_valid():
                kode = request.POST.get('kode')
                nama_status = request.POST.get('nama_status')

                cursor = connection.cursor()
                cursor.execute("SET SEARCH_PATH TO SIVAX;")
                query = """
                    update status_tiket set nama_status = '{}' where kode = '{}';
                """.format(nama_status, kode)
                cursor.execute(query)
                messages.success(request, "Data berhasil diubah")
                return redirect('adminsatgas:masterStatus')

    query = """
    SELECT *
    FROM STATUS_TIKET WHERE kode = '{}'
    """.format(kode)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO SIVAX;")
    cursor.execute(query)
    data_status = dictfetchall(cursor)
    data = {
        'kode' : data_status[0].get('kode'),
        'nama_status' : data_status[0].get('nama_status'),
    }
    form = UpdateStatusTiket(initial=data)
    args = {
        'form' : form,
        'kode' : data_status[0].get('kode'),
        'nama_status' : data_status[0].get('nama_status'),    }
    return render(request,'adminsatgas/updateStatusTiket.html',args)

def daftarVaksin(request):
    query = """
    select * from vaksin;
    """
    cursor = connection.cursor()
    cursor.execute("SET search_path TO sivax;")
    cursor.execute(query)

    vaks = dictfetchall(cursor)

    return render(request, "adminsatgas/daftarVaksin.html", {'vaks': vaks})

def hapusStatusTiket(request, kode):
    with connection.cursor() as cursor:
        cursor = connection.cursor()
        cursor.execute("SET search_path TO SIVAX;")
        cursor.execute("DELETE FROM STATUS_TIKET WHERE kode='{}'".format(kode))
    return redirect('adminsatgas:masterStatus')

def hapusInstansi(request, kode):
    with connection.cursor() as cursor:
        cursor = connection.cursor()
        cursor.execute("SET search_path TO SIVAX;")
        cursor.execute("DELETE FROM INSTANSI WHERE kode='{}'".format(kode))
    return redirect('adminsatgas:masterInstansi')
    

def masterInstansi(request):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to sivax;")
        query = """
            SELECT kode, nama_instansi FROM INSTANSI;
        """
        cursor.execute(query)
        data = dictfetchall(cursor)
       
        response = {
            'datas' : data,
        }
    return render(request, 'adminsatgas/masterInstansi.html', response)

def detailInstansiFaskes(request, kode):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query = """
        select kode_instansi, nama_instansi, tipe, statuskepemilikan
        from instansi, instansi_faskes
        where kode = kode_instansi and  kode = '{}';
        """.format(kode)
        cursor.execute(query)
        data = dictfetchall(cursor)
        args= {
            'kode_instansi' : data[0].get('kode_instansi'),
            'nama_instansi' : data[0].get('nama_instansi'),
            'tipe' : data[0].get('tipe'),
            'statuskepemilikan' : data[0].get('statuskepemilikan'),
        }
    return render(request, 'adminsatgas/detailInstansiFaskes.html', args)

def detailInstansiNonFaskes(request,kode):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query = """
        select kode_instansi, nama_instansi, kategori
        from instansi, instansi_non_faskes
        where kode = kode_instansi and  kode = '{}';
        """.format(kode)
        cursor.execute(query)
        data = dictfetchall(cursor)
        args= {
            'kode_instansi' : data[0].get('kode_instansi'),
            'nama_instansi' : data[0].get('nama_instansi'),
            'kategori' : data[0].get('kategori'),
        }
    return render(request, 'adminsatgas/detailInstansiNonFaskes.html', args)

def updateInstansiFaskes(request, kode):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            form = UpdateInstansi(request.POST)
            if form.is_valid():
                kode_instansi = request.POST.get('kode_instansi')
                nama_instansi = request.POST.get('nama_instansi')
                kategoriInstansi = request.POST.get('kategoriInstansi')
                kategoriTipeFaskes = request.POST.get('kategoriTipeFaskes')
                kategoriStatusKepemilikan = request.POST.get('kategoriStatusKepemilikan')

                cursor = connection.cursor()
                cursor.execute("SET SEARCH_PATH TO SIVAX;")
                query = """
                    update instansi_faskes set kode_instansi = '{}', nama_instansi = '{}' where kode_instansi = '{}';
                """.format(kode_instansi, nama_instansi)
                cursor.execute(query)
                messages.success(request, "Data berhasil diubah")
                return redirect('adminsatgas:masterInstansi')

    query = """
    SELECT *
    FROM instansi_faskes WHERE kode_instansi = '{}'
    """.format(kode)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO SIVAX;")
    cursor.execute(query)
    data_status = dictfetchall(cursor)
    data = {
        'kode_instansi' : data_status[0].get('kode_instansi'),
        'nama_instansi' : data_status[0].get('nama_instansi'),
    }
    form = UpdateInstansi(initial=data)
    args = {
        'form' : form,
        'kode_instansi' : data[0].get('kode_instansi'),
        'nama_instansi' : data[0].get('nama_instansi'),
    }
    return render(request,'adminsatgas/updateInstansiFaskes.html',args)

def updateInstansiNonFaskes(request):
    form2 = KategoriInstansiForm()
    return render(request, 'adminsatgas/updateInstansiNonFaskes.html', {'form2': form2})

def tambahStatus(request, kode, nama_status):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            kode = request.POST.get('kode')
            nama_status = request.POST.get('nama_status')
        
            try:
                #INSERT INTO VAKSIN
                cursor.execute("SET search_path TO sivax;")
                cursor.execute("INSERT INTO STATUS_VAKSIN(kode, nama_status)"
                                "VALUES ('{kode_instansi}', '{nama_status}');".format(kode, nama_status))

            except Exception as e:
                query = """
                SELECT *
                FROM STATUS_VAKSIN where kode = '{}';   
                """.format(kode)

                cursor = connection.cursor()
                cursor.execute("SET search_path TO sivax;")
                cursor.execute(query)

                psdf = dictfetchall(cursor)
                if (len(psdf)!=0):
                    messages.error(request, 'Status sudah pernah terdaftar!')
                else:
                    messages.error(request, 'Status gagal ditambahkan, Coba Lagi!')
                return redirect('adminsatgas:pembuatanTiket')

            return HttpResponseRedirect('/adminsatgas/masterStatus')


