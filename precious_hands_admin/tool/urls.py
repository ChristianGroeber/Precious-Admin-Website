from django.conf.urls import url
from django.urls import path

from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    url('/tool/logout/', views.user_logout, name='logout'),
    path('tool/', views.index, name='index'),
    path('tool/donation_plan/donate/<id>/', views.donate),
    path('tool/donation_plan/donate/', views.donate),
    # path('tool/user/create/', views.create_user),
    path('tool/<option>/create/', views.create),
    path('tool/<option>/view/', views.view),
    path('tool/user/edit/me/', views.edit_user),
    path('tool/<option>/edit/<id>/', views.edit),
    path('tool/import/', views.import_data, name='import_data'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
