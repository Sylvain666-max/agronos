from django.urls import path
from . import views

urlpatterns = [
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
]
