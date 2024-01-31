from django.http import response
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import HttpResponseRedirect
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your views here.
def detailJadwalTiket(request):
    email = request.session.get('email')
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query = f"""
            select kode_instansi, no_tiket, nama_instansi, tgl_waktu, nama_status
            from tiket as t, warga as w, instansi as i, status_tiket as s
            where t.email=w.email and t.kode_instansi=i.kode and t.kode_status=s.kode and t.email='{email}'
        """
        cursor.execute(query)
        data = cursor.fetchone()
        response = {
            'datas' : data,
        }
    return render(request, 'pengguna/detailJadwalTiket.html', response)

def detailJadwalVaksin(request, kode_instansi, tanggal_waktu):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query = f"""
            select nama_instansi, tanggal_waktu, jumlah, kategori_penerima, nama, kode_instansi
            from penjadwalan as p, instansi as i, lokasi_vaksin as l
            where p.kode_instansi=i.kode and p.kode_lokasi=l.kode and tanggal_waktu='{tanggal_waktu}' and kode_instansi='{kode_instansi}'
        """
        cursor.execute(query)
        data = cursor.fetchone()

        query2 = f"""
            select no_tiket
            from tiket
        """

        cursor.execute(query2)
        data2 = dictfetchall(cursor)

        code = int(data2[-1]['no_tiket'][3:]) + 1

        response = {
            'datas': data,
            'no_tiket': "tkt"+str(code),
        }
        return render(request, 'pengguna/detailJadwalVaksin.html', response)

def jadwalVaksin(request):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query = f"""
            SELECT nama_instansi, kode_instansi, tanggal_waktu, jumlah
            FROM PENJADWALAN AS P, INSTANSI AS I
            WHERE P.KODE_INSTANSI=I.KODE
            ORDER BY tanggal_waktu ASC;
        """
        cursor.execute(query)
        data = dictfetchall(cursor)
       
        response = {
            'datas' : data,
        }
        return render(request, 'pengguna/jadwalVaksin.html',response)

def tiketSaya(request):
    email = request.session.get('email')
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query = f"""
            select kode_instansi, no_tiket, nama_instansi, tgl_waktu, nama_status
            from tiket t, warga w, instansi i, status_tiket s
            where w.email=t.email and t.kode_status=s.kode and t.kode_instansi=i.kode and t.email='{email}'
        """
        cursor.execute(query)
        data = dictfetchall(cursor)
        response = {
            'datas' : data,
        }
        return render(request, 'pengguna/tiketSaya.html', response)

def listKartuVaksin(request):
    email = request.session.get('email')
    with connection.cursor() as cursor:
        print(email)
        query = """
        select no_sertifikat,status_tahapan
        from kartu_vaksin where email = '{}';
        """.format(email)
        cursor = connection.cursor()
        cursor.execute("SET search_path TO sivax;")
        cursor.execute(query)

        kartus = dictfetchall(cursor)

        return render(request, 'pengguna/listKartuVaksin.html', {'kartus': kartus})

def detailKartuVaksin(request,no_sertifikat):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query = """
        select w.nama_lengkap, kv.no_sertifikat, kv.status_tahapan
        from kartu_vaksin kv join warga w on kv.email = w.email
        where kv.no_sertifikat = '{}';
        """.format(no_sertifikat)
        cursor.execute(query)
        data = dictfetchall(cursor)
        args= {
            'nama_lengkap' : data[0].get('nama_lengkap'),
            'no_sertifikat' : data[0].get('no_sertifikat'),
            'status_tahapan' : data[0].get('status_tahapan'),
        }
    return render(request, 'pengguna/detailKartuVaksin.html', args)

def daftarVaksin(request):
    return render(request, 'pengguna/daftarVaksin.html')

def tambahTiket(request, kode_instansi, tanggal_waktu, no_tiket):
    email = request.session.get('email')
    with connection.cursor() as cursor:
        try:
            cursor.execute("SET search_path to SIVAX;")
            query = f"""
                insert into tiket (email, no_tiket, kode_instansi, kode_status, tgl_waktu)
                values ('{email}', '{no_tiket}', '{kode_instansi}', '1', '{tanggal_waktu}')
            """

            cursor.execute(query)
        except Exception as e:
            query = f"""
                select *
                from tiket
                where email='{email}' and no_tiket='{no_tiket}'
            """
            cursor.connection.cursor()
            cursor.execute("SET search_path to SIVAX;")
            cursor.execute(query)

            psdf = dictfetchall(cursor)

            print(psdf)

            if (len(psdf) != 0):
                messages.error(request, 'Tiket sudah terdaftar!')
            else :
                messages.error(request, 'Tiket gagal ditambahkan!')
            return redirect('pengguna:jadwalVaksin')
    return HttpResponseRedirect("/pengguna/tiketSaya")

def downloadKartuVaksin(request,no_sertifikat):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX;")
        query = """
            select w.nama_lengkap, kv.no_sertifikat, kv.status_tahapan
            from kartu_vaksin kv join warga w on kv.email = w.email
            where kv.no_sertifikat = '{}';
        """.format(no_sertifikat)
        cursor.execute(query)
        data = dictfetchall(cursor)
        nama_lengkap = data[0].get('nama_lengkap')
        status_tahapan = data[0].get('status_tahapan')
        
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, bottomup = 0)
    textob = p.beginText()
    textob.setTextOrigin(30,30)
    textob.setFont("Helvetica",14)

    lines = [
        "Nama : " + nama_lengkap,
        "No Sertifikat : " + no_sertifikat,
        "Status Tahapan : " + status_tahapan,
    ]

    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename='kartuVaksinSaya.pdf')