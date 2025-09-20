from django.urls import path
from agro_site.core import views

urlpatterns = [
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
]
