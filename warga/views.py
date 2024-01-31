from django.shortcuts import render,redirect
from django.http import HttpResponse, request
from django.db import connection
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


def profilWarga(request):
    email = request.session.get('email')
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to sivax;")
        cursor.execute("SELECT * FROM warga WHERE email = '{}';".format(email))
        data = cursor.fetchone()
        print(data)
        args = {
            'data' : data,
        }
        return render(request, 'warga/profilWarga.html', args)