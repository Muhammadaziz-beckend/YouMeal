from django.contrib import admin

from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'user',
        'count_product',
        'final_tootle_prise',
        'is_see_user'
    ]

    list_display_links = [
        'id',
        'product',
        'user',
        'count_product',
        'final_tootle_prise'
    ]

    list_editable = ['is_see_user']
    readonly_fields = ['final_tootle_prise']
    search_fields = ['product','user','count_product']