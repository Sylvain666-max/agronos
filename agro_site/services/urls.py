from django.urls import path
from . import views

app_name = 'agro_site.services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<slug:slug>/', views.service_detail, name='service_detail'),
    path('checkout/<int:service_id>/', views.create_checkout_session, name='service_checkout'),
    path('success/', views.success_payment, name='success_payment'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]