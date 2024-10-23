from django.contrib import admin
from .models import Order, PromotionalCode


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'user',
        'count',
        'status',
        'total_price',
        'promo_code',
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
        'promo_code',
        'date_create',
        'date_update'
    ]

    readonly_fields = [
        'total_price','status',
    ]

    search_fields = ['user__phone', 'status', 'date_create', 'date_update']

    list_filter = ['status','promo_code']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return []
        return ['total_price', 'status']


@admin.register(PromotionalCode)
class PromotionalCodeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code',
        'discount_type',
        'subtraction_from_the_amount',
        'data_start',
        'data_end',
        'is_active'
    ]

    list_display_links = [
        'id',
        'code',
        'discount_type',
        'subtraction_from_the_amount',
        'data_start',
        'data_end',
    ]

    list_editable = ['is_active']
    search_fields = [
        'code',
        'discount_type',
        'subtraction_from_the_amount',
        'data_start',
        'data_end',
    ]
    list_filter = ['discount_type']