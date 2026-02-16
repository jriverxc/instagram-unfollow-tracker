from django.urls import path

from .views import download_csv, index

urlpatterns = [
    path('', index, name='index'),
    path('download-csv/', download_csv, name='download_csv'),
]
