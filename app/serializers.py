from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, SubCategory, Product, Pricing, ProductSpesfication


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('name', )

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'series', 'manfacturer', 'origin', 'eg_stock', 'ae_stock', 'tr_stock')

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ('product', 'eg_buy_price', 'eg_cost', 'eg_profit',
                   'ae_buy_price', 'ae_cost', 'ae_profit', 'tr_buy_price',
                     'tr_cost', 'tr_profit', 'eg_final_price', 'ae_final_price',
                       'tr_final_price')


class ProductSpesficationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpesfication
        fields = '__all__'
