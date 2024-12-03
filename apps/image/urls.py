from django.urls import path
from . import views
from ..oaauth.urls import app_name

app_name="image"

urlpatterns= [
    path('upload', views.UploadImageView.as_view(), name='upload'),
]