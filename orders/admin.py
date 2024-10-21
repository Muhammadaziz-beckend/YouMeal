from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'user',
        'count',
        'status',
        'total_price',
        'date_create',
        'date_update'
    ]

    list_display_links = [
        'id',
        'product',
        'user',
        'count',
        'status',
        'total_price',
        'date_create',
        'date_update'
    ]

    readonly_fields = [
        'total_price','status',
    ]

    search_fields = ['user__phone', 'status', 'date_create', 'date_update']

    list_filter = ['status']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return []
        return ['total_price', 'status']
