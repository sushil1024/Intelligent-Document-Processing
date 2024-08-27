from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('input', views.inputdata, name='input'),
    path('documents/', views.documentprocess, name='process')
]


