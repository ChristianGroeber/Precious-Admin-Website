from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('tool/', views.index, name='index'),
    path('tool/<option>/create/', views.create),
    path('tool/<option>/view/', views.view),
    path('tool/<option>/edit/<id>/', views.edit),
]
