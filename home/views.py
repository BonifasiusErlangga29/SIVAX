from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate
from django.db import connection
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse

def fetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def cek_peran(email, peran):
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO SIVAX;")
        query = "SELECT * FROM " + peran + " WHERE email = %s;"
        cursor.execute(query, [email])
        row = fetchall(cursor)

        if len(row) != 0:
            return True
        else:
            return False

# Create your views here.
def index(request):
    return render(request, 'home/index.html')
    
def login(request):
    with connection.cursor() as cursor:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]

                cursor.execute("SET SEARCH_PATH TO SIVAX;")
                cursor.execute("SELECT * FROM PENGGUNA WHERE " + "email = %s AND password = %s;", [email, password])


                user = fetchall(cursor)
                print(user)

                if len(user) != 0:
                    user = user[0]
                    request.session["email"] = user["email"]

                    if cek_peran(email, "nakes"):
                        request.session["peran"] = "nakes"
                    elif cek_peran(email, "panitia_penyelenggara"):
                        request.session["peran"] = "panitia_penyelenggara"
                    elif cek_peran(email, "admin_satgas"):
                        request.session["peran"] = "admin_satgas"
                    elif cek_peran(email, "warga"):
                        request.session["peran"] = "warga"

                    peranSekarang = request.session["peran"]
                    if peranSekarang == "admin_satgas":
                        return redirect('adminsatgas:profilAdminSatgas')
                    elif peranSekarang == "nakes":
                        return redirect('nakes:profilNakes')
                    elif peranSekarang == "panitia_penyelenggara":
                        return redirect('panitiapenyelenggara:profilPanitiaPenyelenggara')
                    elif peranSekarang == "warga":
                        return redirect('warga:profilWarga')

                messages.error(request, 'Username atau Password yang anda masukkan salah!')
                return redirect('home:login')
        else:
            form = LoginForm()
            return render(request, "home/login.html", {'form': form})

def register(request):
    return render(request, "home/register.html")

def registerAdminSatgas(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            form = RegisterAdminSatgasForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                password = request.POST.get('password')
                noHp = request.POST.get('noHp')
                nomorPetugas = request.POST.get('nomorPetugas')
                nik = request.POST.get('nik')
                namaPanjang = request.POST.get('namaPanjang')
                jenisKelamin = request.POST.get('jenisKelamin')
                nomorBangunan = request.POST.get('nomorBangunan')
                namaJalan = request.POST.get('namaJalan')
                kelurahan = request.POST.get('kelurahan')
                kecamatan = request.POST.get('kecamatan')
                kotaAdministrasi = request.POST.get('kotaAdministrasi')
                instansi = request.POST.get('instansi')
                peran = 'admin_satgas'

                try:
                    #INSERT INTO PENGGUNA
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute("INSERT INTO PENGGUNA(email, no_telp, password, status_verifikasi)"
                                    "VALUES ('{}', '{}', '{}', 'belum terverifikasi');".format(email, noHp, password))

                    #INSERT INTO ADMIN SATGAS
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute("INSERT INTO ADMIN_SATGAS(id_pegawai,email)"
                                    "VALUES ('{}', '{}');".format(nomorPetugas, email))

                    #INSERT INTO WARGA
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute("INSERT INTO WARGA(email, nik, nama_lengkap, jenis_kelamin, no, jalan, kelurahan, kecamatan, kabkot, instansi)"
                                    "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(email, nik, namaPanjang, jenisKelamin, nomorBangunan, namaJalan, kelurahan, kecamatan, kotaAdministrasi, instansi))
                
                except Exception as e:
                    query = """
                    SELECT *
                    FROM pengguna where email = '{}';   
                    """.format(email)

                    print(e)
                    cursor = connection.cursor()
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute(query)

                    psdf = dictfetchall(cursor)
                    if (len(psdf)!=0):
                        messages.error(request, 'Username sudah pernah terdaftar!')
                    else:
                        messages.error(request, 'Password harus mengandung 1 angka dan 1 huruf kapital!')
                    return redirect('home:registerAdminSatgas')

                request.session['email'] = email
                request.session["peran"] = "admin_satgas"
                return redirect('adminsatgas:profilAdminSatgas')

    form = RegisterAdminSatgasForm()
    args = {
        'form' : form,
    }
    return render(request, 'home/registerAdminSatgas.html', args)

def registerPanitiaPenyelenggara(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            form = RegisterPanitiaPenyelenggaraForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                password = request.POST.get('password')
                noHp = request.POST.get('noHp')
                namaPanjang = request.POST.get('namaPanjang')
                isTenagaKesehatan = request.POST.get('isTenagaKesehatan')
                nomorSTR = request.POST.get('nomorSTR')
                tipePetugas = request.POST.get('tipePetugas')
                nik = request.POST.get('nik')
                jenisKelamin = request.POST.get('jenisKelamin')
                nomorBangunan = request.POST.get('nomorBangunan')
                namaJalan = request.POST.get('namaJalan')
                kelurahan = request.POST.get('kelurahan')
                kecamatan = request.POST.get('kecamatan')
                kotaAdministrasi = request.POST.get('kotaAdministrasi')
                instansi = request.POST.get('instansi')
                peran = 'panitia_penyelenggara'

                try:
                    #INSERT INTO PENGGUNA
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute("INSERT INTO PENGGUNA(email, no_telp, password, status_verifikasi)"
                                    "VALUES ('{}', '{}', '{}', 'belum terverifikasi');".format(email, noHp, password))

                    #INSERT INTO PANITIA PENYELENGGARA
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute("INSERT INTO PANITIA_PENYELENGGARA(email,nama_lengkap)"
                                    "VALUES ('{}', '{}');".format(email,namaPanjang))

                    #INSERT INTO WARGA
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute("INSERT INTO WARGA(email, nik, nama_lengkap, jenis_kelamin, no, jalan, kelurahan, kecamatan, kabkot, instansi)"
                                    "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(email, nik, namaPanjang, jenisKelamin, nomorBangunan, namaJalan, kelurahan, kecamatan, kotaAdministrasi, instansi))
                    
                    #INSERT INTO NAKES
                    if (isTenagaKesehatan == 'yes'):

                        cursor.execute("SET search_path TO sivax;")
                        cursor.execute("INSERT INTO nakes(email, no_str, tipe)"
                                        "VALUES ('{}', '{}', '{}');".format(email, nomorSTR, tipePetugas))

                except Exception as e:
                    query = """
                    SELECT *
                    FROM pengguna where email = '{}';   
                    """.format(email)

                    print(e)
                    cursor = connection.cursor()
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute(query)

                    psdf = dictfetchall(cursor)
                    if (len(psdf)!=0):
                        messages.error(request, 'Username sudah pernah terdaftar!')
                    else:
                        messages.error(request, 'Password harus mengandung 1 angka dan 1 huruf kapital!')
                    return redirect('home:registerPanitiaPenyelenggara')

                request.session['email'] = email
                request.session["peran"] = "panitia_penyelenggara"
                if (isTenagaKesehatan == 'yes'):
                    request.session["instansi"] = instansi
                    request.session["peranKedua"] = "nakes"
                return redirect('panitiapenyelenggara:profilPanitiaPenyelenggara')

    form = RegisterPanitiaPenyelenggaraForm()
    args = {
        'form' : form,
    }
    return render(request, 'home/registerpanitiapenyelenggara.html', args)

def registerWarga(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            form = RegisterWargaForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                password = request.POST.get('password')
                noHp = request.POST.get('noHp')
                nik = request.POST.get('nik')
                namaPanjang = request.POST.get('namaPanjang')
                jenisKelamin = request.POST.get('jenisKelamin')
                nomorBangunan = request.POST.get('nomorBangunan')
                namaJalan = request.POST.get('namaJalan')
                kelurahan = request.POST.get('kelurahan')
                kecamatan = request.POST.get('kecamatan')
                kotaAdministrasi = request.POST.get('kotaAdministrasi')
                instansi = request.POST.get('instansi')
                peran = 'admin_satgas'

                try:
                    #INSERT INTO PENGGUNA
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute("INSERT INTO PENGGUNA(email, no_telp, password, status_verifikasi)"
                                    "VALUES ('{}', '{}', '{}', 'belum terverifikasi');".format(email, noHp, password))

                    #INSERT INTO WARGA
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute("INSERT INTO WARGA(email, nik, nama_lengkap, jenis_kelamin, no, jalan, kelurahan, kecamatan, kabkot, instansi)"
                                    "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(email, nik, namaPanjang, jenisKelamin, nomorBangunan, namaJalan, kelurahan, kecamatan, kotaAdministrasi, instansi))
                
                except Exception as e:
                    query = """
                    SELECT *
                    FROM pengguna where email = '{}';   
                    """.format(email)

                    print(e)
                    cursor = connection.cursor()
                    cursor.execute("SET search_path TO sivax;")
                    cursor.execute(query)

                    psdf = dictfetchall(cursor)
                    if (len(psdf)!=0):
                        messages.error(request, 'Username sudah pernah terdaftar!')
                    else:
                        messages.error(request, 'Password harus mengandung 1 angka dan 1 huruf kapital!')
                    return redirect('home:registerWarga')

                request.session['email'] = email
                request.session["peran"] = "warga"
                return redirect('warga:profilWarga')

    form = RegisterWargaForm()
    args = {
        'form' : form,
    }
    return render(request, 'home/registerWarga.html', args)

def logout(request):
    request.session.flush()
    return redirect('home:index')
