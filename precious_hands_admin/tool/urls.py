from django.urls import path

from precious_hands_admin.tool import views

urlpatterns = [
    path('/', views.index, name='index'),
]
