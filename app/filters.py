from django_filters import rest_framework as filters
from .models import Product, ProductSpesfication, Specification

class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='subcategory__category__name', lookup_expr='icontains')
    subcategory = filters.CharFilter(field_name='subcategory__name', lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    series = filters.CharFilter(lookup_expr='icontains')
    manfacturer = filters.CharFilter(lookup_expr='icontains')
    origin = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    eg_stock = filters.NumberFilter()
    ae_stock = filters.NumberFilter()
    tr_stock = filters.NumberFilter()

    # Dynamically add filters for each specification name
    @staticmethod
    def add_specification_filters():
        for specification in Specification.objects.all():
            filter_name = specification.name.lower().replace(' ', '_')
            ProductFilter.base_filters[filter_name] = filters.CharFilter(
                field_name=f'specifications__value',
                method='filter_by_specification_value',
                label=specification.name
            )

    def filter_by_specification_value(self, queryset, name, value):
        specification_name = name.replace('_', ' ').capitalize()
        return queryset.filter(
            specifications__specification__name__iexact=specification_name,
            specifications__value__iexact=value
        )

    class Meta:
        model = Product
        fields = [
            'category',
            'subcategory',
            'name',
            'series',
            'manfacturer',
            'origin',
            'description',
            'eg_stock',
            'ae_stock',
            'tr_stock',
        ]

# Call this function to add the specification filters dynamically
# ProductFilter.add_specification_filters()
