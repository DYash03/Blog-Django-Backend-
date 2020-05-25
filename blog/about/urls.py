from django.urls import path
from . import views
app_name = 'about'

urlpatterns = [
    path('', views.about, name='about'),
    path('author/<slug:slug>', views.author, name='author'),
]
