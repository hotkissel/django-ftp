from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main'),
    path('downloads', views.downloads, name='downloads'),
    path('news', views.news, name='news'),
    path('js/date_convert.js', views.js, name='js'),
    path('upload_from_computer', views.upload_from_computer, name='upload_from_computer'),
    path('upload_from_url', views.upload_from_url, name='upload_from_url'),
    path('upload', views.upload, name='upload')
]