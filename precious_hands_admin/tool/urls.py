from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('tool/', views.index, name='index'),
    path('tool/create/<option>/', views.create),
    path('tool/view/<option>/', views.view),
    path('tool/edit/<option>/<id>/', views.edit),
]
