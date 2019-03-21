from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('tool/', views.index, name='index'),
    path('create/<option>/', views.create),
]
