from django.urls import path
from . import views

app_name = 'agro_site.shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('categorie/<slug:category_slug>/', views.product_list, name='product_by_category'),
    path('produit/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.product_list, name='search'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/order/<int:order_id>/', views.checkout_order, name='checkout_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/cancel/<int:order_id>/', views.order_cancel, name='order_cancel'),
]
