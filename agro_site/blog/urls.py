from django.urls import path
from agro_site.blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('categorie/<slug:category_slug>/', views.post_list, name='post_by_category'),
    path('article/<slug:slug>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('formation/checkout/<int:post_id>/', views.post_checkout, name='post_checkout'),
    path("mes-formations/", views.my_courses, name="my_courses"),
    path("checkout/cancel/",views.checkout_cancel,name='cancel'),
    path("stripe/webhook/",views.stripe_webhook,name='stripe_webhook'),
]
