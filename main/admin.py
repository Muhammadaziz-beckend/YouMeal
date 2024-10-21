from django.contrib import admin
from .models import *


class Product_compositionAdmin(admin.StackedInline):
    model = Product_composition
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'calories', 'price', 'category']
    list_display_links = ['id', 'name', 'calories', 'price', 'category']
    list_filter = ['category','product']
    inlines = [Product_compositionAdmin]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name',]
    list_display_link = ['id','name',]
