from django.contrib import admin
from .models import Order, PromotionalCode, Address


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'status',
        'type_order',
        'total_price',
        'promo_code',
        'date_create',
        'date_update'
    ]

    list_display_links = [
        'id',
        'user',
        'status',
        'type_order',
        'total_price',
        'promo_code',
        'date_create',
        'date_update'
    ]

    readonly_fields = [
        'total_price','status','cart'
    ]

    search_fields = ['user__phone', 'status', 'date_create', 'date_update']

    list_filter = ['status','promo_code','type_order']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['cart']
        return ['total_price', 'status','cart']


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


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'street',
        'house_number',
        'apartment',
        'floor',
        'intercom',
        'create_data',
    ]

    list_display_links = [
        'id',
        'user',
        'street',
        'house_number',
        'apartment',
        'floor',
        'intercom',
        'create_data',
    ]

    list_filter = ['user']
    search_fields = ['user__phone','street','house_number']
