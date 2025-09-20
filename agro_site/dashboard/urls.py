from django.urls import path
from agro_site.dashboard import views

app_name = 'agro_site.dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),


    # Articles
    path('article/add/', views.add_Post, name='dashboard_add_article'),
    path('articles/', views.list_Post, name='dashboard_list_articles'),
    path('article/edit/<int:pk>/', views.edit_article, name='dashboard_edit_article'),
    path('article/delete/<int:pk>/', views.delete_article, name='dashboard_delete_article'),

    # Products
    path('product/add/', views.add_product, name='dashboard_add_product'),
    path('products/', views.list_products, name='dashboard_list_products'),
    path('product/edit/<int:pk>/', views.edit_product, name='dashboard_edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='dashboard_delete_product'),

    # Services
    path('service/add/', views.add_service, name='dashboard_add_service'),
    path('services/', views.list_services, name='dashboard_list_services'),
    path('service/edit/<int:pk>/', views.edit_service, name='dashboard_edit_service'),
    path('service/delete/<int:pk>/', views.delete_service, name='dashboard_delete_service'),
]
