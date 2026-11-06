
from django.urls import path
from . import views
app_name='core'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('timeline/', views.timeline_page, name='timeline'),
    path('administration', views.admin_page, name='admin_page'),
    path('show_cars_admin', views.show_cars_admin, name='show_cars_admin'),
    path('car_details<int:id>/', views.car_details, name='car_details'),
    path('admin_search_voiture', views.admin_search_voiture, name='admin_search_voiture'),
    path('admin_search_car', views.admin_search_car, name='admin_search_car'),
    path('basculer_type<int:id>/',views.basculer_type, name='basculer_type'),
    path('edit_car<int:id>/',views.edit_car, name='edit_car'),
    path('change_disponibilite<int:id>/',views.change_disponibilite, name='change_disponibilite'),
    path('delete_car<int:id>/',views.delete_car, name='delete_car'),
    path('admin_manage_user', views.admin_manage_user, name='admin_manage_user'),
    path('block_unblock_user<int:id>/',views.block_unblock_user, name='block_unblock_user'),
    path('delete_user<int:id>/',views.delete_user, name='delete_user'),
    path('view_user<int:id>/',views.view_user, name='view_user'),
    path('admin_search_user', views.admin_search_user, name='admin_search_user'),
    path('repondre<int:id>/',views.repondre, name='repondre'),
    path('action_admin',views.action_admin, name='action_admin'),
    path('search_action',views.search_action, name='search_action'),
    path('contact_client/<int:id>/',views.contact_client, name='contact_client')
    
]   
