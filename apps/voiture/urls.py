
from django.urls import path
from . import views

app_name = "voitures"

urlpatterns = [
    path('room/', views.show_voitures, name='show_voitures'),
    path('vente_car/', views.vente_car, name='vente_car'),
    path('search_car_achat/', views.search_car_achat, name='search_car_achat'),
    path('location_car/', views.location_car, name='location_car'),
    path('search_car_location/', views.search_car_location, name='search_car_location'),
    path("buy_car/<int:id>/", views.buy_car,name='buy_car'),
    path("payment-success/", views.success,name='success'),
    path("payment-cancel/", views.cancel,name='cancel'),
    path("delete_all_cars/", views.delete_all_cars,name='delete_all_cars'),
    path("add_voiture/", views.add_voiture,name='add_voiture'),
    path("recherche_voitures/", views.recherche_voitures,name='recherche_voitures'),
    path("add_voiture_photo/<int:id>/", views.add_voiture_photo, name='add_voiture_photo'),

]