
from django.urls import path

from Hagesh2 import views

urlpatterns = [
    path('', views.index, name='index'),
    path('letter/',views.letter,name="letter"),
    path('home/', views.home, name='home'),
    path('download_file/', views.download_file, name='download_file'),
    path('form/', views.form, name='form'),


]
