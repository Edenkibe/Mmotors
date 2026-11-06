
from django.urls import path
from . import views

app_name = "integrations"

urlpatterns = [
    path('webhooks/yousign/',views.yousign_webhook,name='yousign_webhook'),
    path("stripe/webhook/", views.stripe_webhook,name='stripe_webhook'),
  
]