
from django.urls import path
from . import views
app_name='contact'

urlpatterns = [
    path('contact_dossier/', views.contact_dossier, name='contact_dossier'),
    path('success_page/', views.success_page, name='success_page'),
    
]
