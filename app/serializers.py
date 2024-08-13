from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, SubCategory, Product, Pricing, ProductSpesfication, UserProfile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'subcategory', 'name', 'image', 'description', 'series', 'manfacturer', 'origin', 'eg_stock', 'ae_stock', 'tr_stock')

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ('id', 'product', 'eg_buy_price', 'eg_cost', 'eg_profit',
                   'ae_buy_price', 'ae_cost', 'ae_profit', 'tr_buy_price',
                     'tr_cost', 'tr_profit', 'eg_final_price', 'ae_final_price',
                       'tr_final_price')


class ProductSpesficationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpesfication
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'kind']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user