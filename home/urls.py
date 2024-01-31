from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('registerAdminSatgas', views.registerAdminSatgas, name='registerAdminSatgas'),
    path('registerPanitiaPenyelenggara', views.registerPanitiaPenyelenggara, name='registerPanitiaPenyelenggara'),
    path('registerWarga', views.registerWarga, name='registerWarga'),
    path('logout/', views.logout, name = 'logout')
]