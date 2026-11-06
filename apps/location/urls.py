
from django.urls import path
from . import views

app_name = "locations"

urlpatterns = [
  path('creer_dossier_location/<int:id>/', views.creer_dossier_location, name='creer_dossier_location'), 
  path('success_location/', views.success_location, name='success_location'),
  path('get_demande_location/', views.get_demande_location, name='get_demande_location'),
  path('repondre_location/<int:id>', views.repondre_location, name='repondre_location'),
  path('search_location/', views.search_location, name='search_location'),
  path('location_car<int:id>/', views.location_car, name='location_car'),
  path('rejected_location/<int:id>/', views.rejected_location, name='rejected_location'),
  path('check_raison_booking/<int:id>/', views.check_raison_booking, name='check_raison_booking'),
  path('user_search_location/', views.user_search_location, name='user_search_location'),
  path('user_search_achat/', views.user_search_achat, name='user_search_achat'),
  path('live_booking/', views.live_booking, name='live_booking'),
  path('admin_search_ongoing_bookings/', views.admin_search_ongoing_bookings, name='admin_search_ongoing_bookings'),
  path('user_satisfaction_location/<int:id>/', views.user_satisfaction_location, name='user_satisfaction_location'),
  path('user_not_satisfied_location/<int:id>/', views.user_not_satisfied_location, name='user_not_satisfied_location'),
  path('unsuccess_location/', views.unsuccess_location, name='unsuccess_location'),
  path('redirect_after_responding/', views.redirect_after_responding, name='redirect_after_responding'),
]