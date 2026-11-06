
from django.urls import path
from . import views

app_name = "dossiers"

urlpatterns = [
    path('dossier<int:id>/', views.depot_dossier, name='depot_dossier'),
    path('dossier_accepted/', views.dossier_accepted, name='dossier_accepted'),
    path('all_demandes/', views.all_demandes, name='all_demandes'),
    path('search_dossier/', views.search_dossier, name='search_dossier'),
    path('all_sold_demand/', views.all_sold_demand, name='all_sold_demand'),
    path('search_sold_car/', views.search_sold_car, name='search_sold_car'),
    path('success_dossier_depot/', views.success_dossier_depot, name='success_dossier_depot'),
    path('rejected_notification/<int:id>/', views.rejected_notification, name='rejected_notification'),
    path('check_raison/<int:id>/', views.check_raison, name='check_raison')
]