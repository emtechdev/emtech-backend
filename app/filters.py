import django_filters
from .models import Product, ProductSpesfication, Category, SubCategory

class ProductFilter(django_filters.FilterSet):
    # Filtering by Category and SubCategory
    category = django_filters.ModelChoiceFilter(
        field_name='subcategory__category',
        queryset=Category.objects.all(),
        label='Category'
    )
    subcategory = django_filters.ModelChoiceFilter(
        queryset=SubCategory.objects.all(),
        label='Subcategory'
    )

    # Filtering by Product Fields
    name = django_filters.CharFilter(lookup_expr='icontains')
    series = django_filters.CharFilter(lookup_expr='icontains')
    manfacturer = django_filters.CharFilter(lookup_expr='icontains')
    origin = django_filters.CharFilter(lookup_expr='icontains')
    eg_stock = django_filters.NumberFilter()
    ae_stock = django_filters.NumberFilter()
    tr_stock = django_filters.NumberFilter()

    # Filtering by Product Specifications
    # Assuming specifications are key-value pairs
    # We'll use a method to filter based on specifications
    specification = django_filters.CharFilter(method='filter_specification')

    class Meta:
        model = Product
        fields = [
            'category', 'subcategory', 'name', 'series', 'manfacturer', 'origin',
            'eg_stock', 'ae_stock', 'tr_stock', 'specification'
        ]

    def filter_specification(self, queryset, name, value):
        # Expecting value in the format "spec_name:spec_value"
        try:
            spec_name, spec_value = value.split(':')
            return queryset.filter(
                productspesfication__name__iexact=spec_name.strip(),
                productspesfication__value__iexact=spec_value.strip()
            )
        except ValueError:
            return queryset