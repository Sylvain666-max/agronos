from django.contrib import admin
from .models import Service, QuoteRequest

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'price_from')
    search_fields = ('name', 'description')

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('service', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    list_filter = ('created_at', 'service')
