from django.urls import path
from . import views

urlpatterns = [

    path('create/', views.create, name='create'),
    path('toggle/', views.toggle, name='toggle'),
    path('destroy/', views.destroy, name='destroy'),
    path('', views.index, name='index')
]
