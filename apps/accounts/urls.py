
from django.urls import path
from . import views
app_name='accounts'
urlpatterns = [
    path('register/', views.registration, name='registration'),
    path('admin-register/', views.admin_user_registration, name='admin_user_registration'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success, name='success'),
    path('failed/', views.failed, name='failed'),
    path('success_registration/', views.success_registration, name='success_registration'),
    path('failed_registration/', views.failed_registration, name='failed_registration'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profil/', views.user_profil, name='user_profil'),
    path("change-password/",views.change_password,name="change_password"),
    path("info-modification/",views.info_modification,name="info_modification"),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('sent_mail_reset_password/', views.sent_mail_reset_password, name='sent_mail_reset_password'),
    path('user_info/', views.user_info, name='user_info'),
    path('user_all_request/', views.user_all_request, name='user_all_request'),
    path('delete_all_users/', views.delete_all_user, name='delete_all_user'),
    path('user_location_request/', views.user_location_request, name='user_location_request')
]
