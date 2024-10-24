from django_filters import rest_framework as django_filters
from main.models import Product,Category

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(),to_field_name='id',
        label='Категории')

    class Meta:
        model = Product
        fields = [
            'category',
            'calories',
            'product_composition',
            'is_publish',
            'weight',
            'name',
            'description'
        ]
