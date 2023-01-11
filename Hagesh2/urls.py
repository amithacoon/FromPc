
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Hagesh2 import views

urlpatterns = [
    path('', views.index, name='index'),
    path('letter/',views.letter,name="letter"),
    path('home/', views.home, name='home'),
    path('download_file/', views.download_file, name='download_file'),
    path('form/', views.form, name='form'),
    path('upload_photo/', views.upload_photo, name='upload_photo'),
    path('replace/', views.replace_pic, name='replace_pic'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)