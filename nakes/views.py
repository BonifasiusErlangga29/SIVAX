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


def profilNakes(request):
    email = request.session.get('email')
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to sivax;")
        cursor.execute("SELECT * from nakes WHERE email = '{}';".format(email))
        data = cursor.fetchone()
        print(data)
        args = {
            'data' : data,
        }
        return render(request, 'nakes/profilNakes.html', args)


def listTiket(request):
    instansi = request.session.get("instansi")
    query = """
    select t.no_tiket,w.nama_lengkap,t.tgl_waktu,
    st.nama_status from tiket t join warga w on
    t.email = w.email join status_tiket as st 
    on t.kode_status = st.kode where t.kode_instansi = '{}';
    """.format(instansi)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO sivax;")
    cursor.execute(query)

    tikets = dictfetchall(cursor)

    return render(request, 'nakes/listTiket.html', {'tikets': tikets})

def detailTiket(request,no_tiket):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query = """
        select t.no_tiket,w.nama_lengkap,t.tgl_waktu,
        st.nama_status from tiket t join warga w on
        t.email = w.email join status_tiket as st 
        on t.kode_status = st.kode where t.no_tiket = '{}';
        """.format(no_tiket)
        cursor.execute(query)
        data = dictfetchall(cursor)
        args= {
            'nama_lengkap' : data[0].get('nama_lengkap'),
            'tgl_waktu' : data[0].get('tgl_waktu'),
            'nama_status' : data[0].get('nama_status'),
            'no_tiket' : data[0].get('no_tiket'),
        }
        return render(request, 'nakes/detailTiket.html', args)

def updateTiket(request,no_tiket):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            form = UpdateTiketForm(request.POST)
            if form.is_valid():
                no_tiket = no_tiket
                if (request.POST.get('statusTiket')=='terdaftar'):
                    status = 1
                elif (request.POST.get('statusTiket')=='siap vaksin'):
                    status = 2
                elif (request.POST.get('statusTiket')== 'tidak lolos screeening'):
                    status = 3
                else:
                    status = 4
                cursor = connection.cursor()
                cursor.execute("SET search_path TO sivax;")
                cursor.execute("UPDATE tiket SET kode_status = '{}' WHERE"
                                " no_tiket = '{}';".format(status,no_tiket))
                return redirect('nakes:listTiket')
        
    query = """
    SELECT i.nama_instansi, t.tgl_waktu, p.jumlah,
    p.kategori_penerima, lv.nama as lokasi_vaksin, t.no_tiket
    FROM tiket t join penjadwalan p on t.kode_instansi = p.kode_instansi
    join lokasi_vaksin lv on p.kode_lokasi = lv.kode join instansi i
    on p.kode_instansi = i.kode
    WHERE t.no_tiket = '{}'
    """.format(no_tiket)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO sivax;")
    cursor.execute(query)
    data_temp = dictfetchall(cursor)
    # if (data_temp[0].get('kode_status'))
    data = {
        'nama_instansi' : data_temp[0].get('nama_instansi'),
        'tgl_waktu' : data_temp[0].get('tgl_waktu'),
        'jumlah' : data_temp[0].get('jumlah'),
        'kategori_penerima' : data_temp[0].get('kategori_penerima'),
        'lokasi_vaksin' : data_temp[0].get('lokasi_vaksin'),
        'no_tiket' : data_temp[0].get('no_tiket'),
    }
    form = UpdateTiketForm(initial=data)
    args = {
        'form' : form,
        'nama_instansi' : data_temp[0].get('nama_instansi'),
        'tgl_waktu' : data_temp[0].get('tgl_waktu'),
        'jumlah' : data_temp[0].get('jumlah'),
        'kategori_penerima' : data_temp[0].get('kategori_penerima'),
        'lokasi_vaksin' : data_temp[0].get('lokasi_vaksin'),
        'no_tiket' : data_temp[0].get('no_tiket'),
    }
    return render(request, 'nakes/updateTiket.html', args)
