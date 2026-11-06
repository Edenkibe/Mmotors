
from django.urls import path
from . import views
app_name='promotion'
urlpatterns = [
    path('create_promotion<int:id>/',views.create_promotion, name='create_promotion'),
    path('view_all_ads/',views.view_all_ads, name='view_all_ads'),
    path('bloque_unbloque<int:id>/',views.bloque_unbloque, name='bloque_unbloque'),
    path('delete_ads<int:id>/',views.delete_ads, name='delete_ads'),
    path('modifier_pub<int:id>/',views.modifier_pub, name='modifier_pub'),
    path('admin_search_ads/',views.admin_search_ads, name='admin_search_ads'),
]
