from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction

from .models import (Category, SubCategory, Product, 
                     Pricing, ProductSpesfication, UserProfile,
                       File, Image, PurchaseBill ,
                         PurchaseBillItem, SalesBill,
                           SalesBillItem, ProductBill ,
                             ProductBillItem, Specification,
                               ProductSpesfication, Trader, Customer)


class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = '__all__'




class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'




class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['id', 'name', 'value']




class ProductSpesficationSerializer(serializers.ModelSerializer):
    specification_name = serializers.CharField(source='specification.name', read_only=True)
    specification_value = serializers.CharField(source='value', read_only=True)

    class Meta:
        model = ProductSpesfication
        fields = ('id','specification_name', 'specification_value')




class SubCategorySerializer(serializers.ModelSerializer):
    specifications = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category', 'specifications']




class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'




class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'image_url', 'image']

    def get_image_url(self, obj):
        return obj.image.url




class ProductSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    image = ImageSerializer()
    specifications = ProductSpesficationSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = (
            'id', 'subcategory', 'file_url', 'file', 'name',
            'image', 'description', 'series',
            'manfacturer', 'origin', 'eg_stock',
            'ae_stock', 'tr_stock', 'specifications'
        )


    def get_file_url(self, obj):
        if obj.file:
            return obj.file.file.url
        return None

    



class PricingSerializer(serializers.ModelSerializer):
    final_prices = serializers.SerializerMethodField()


    class Meta:
        model = Pricing
        fields = (
            'id', 'product', 'time',
            'eg_buy_price', 'eg_cost', 'eg_profit',
            'ae_buy_price', 'ae_cost', 'ae_profit',
            'tr_buy_price', 'tr_cost', 'tr_profit',
            'usd_to_egp', 'usd_to_eur', 'usd_to_tr', 'usd_to_rs', 'usd_to_ae', 'usd_to_strlini',
            'final_prices'
        )


    def get_final_prices(self, obj):
        currencies = ['USD', 'EGP', 'EUR', 'TR', 'RS', 'AE', 'STRLINI']
        locations = ['EG', 'AE', 'TR']
        final_prices = {}

        for location in locations:
            for currency in currencies:
                try:
                    final_prices[f'{location}_{currency}'] = obj.get_final_price(location, currency)
                except ValueError:
                    final_prices[f'{location}_{currency}'] = None  # Or handle errors as needed

        return final_prices




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'kind']




class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(source='userprofile', read_only=True)


    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ['username', 'password', 'user_profile']  


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    



class PurchaseBillItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()


    class Meta:
        model = PurchaseBillItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'location']




class PurchaseBillSerializer(serializers.ModelSerializer):
    items = PurchaseBillItemSerializer(many=True, read_only=True)
    trader = TraderSerializer(read_only=True)  # Add trader data


    class Meta:
        model = PurchaseBill
        fields = ['id', 'name', 'purchase_date', 'total_price', 'items', 'trader'] 




class SalesBillItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # This includes all product details


    class Meta:
        model = SalesBillItem
        fields = ['product', 'quantity', 'location', 'unit_price']




class SalesBillSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)  # Ensure you have CustomerSerializer defined
    items = SalesBillItemSerializer(source='salesbillitem_set', many=True, read_only=True)


    class Meta:
        model = SalesBill
        fields = ['id', 'customer', 'name', 'sales_date', 'total_price', 'items', 'status']


    def create(self, validated_data):
        items_data = self.context['request'].data.get('items', [])
        sales_bill = SalesBill.objects.create(**validated_data)

        total_price = 0
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product']['id'])
            quantity = item_data['quantity']
            location = item_data['location']
            unit_price = product.unit_price  # Ensure this field is available on the product

            # Check stock availability
            if location == 'EG':
                if product.eg_stock < quantity:
                    raise serializers.ValidationError(f"Not enough stock for product {product.name} in Egypt.")
                product.eg_stock -= quantity
            elif location == 'AE':
                if product.ae_stock < quantity:
                    raise serializers.ValidationError(f"Not enough stock for product {product.name} in UAE.")
                product.ae_stock -= quantity
            elif location == 'TR':
                if product.tr_stock < quantity:
                    raise serializers.ValidationError(f"Not enough stock for product {product.name} in Turkey.")
                product.tr_stock -= quantity
            
            product.save()

            # Create SalesBillItem
            SalesBillItem.objects.create(
                sales_bill=sales_bill,
                product=product,
                quantity=quantity,
                location=location
            )

            total_price += quantity * unit_price

        sales_bill.total_price = total_price
        sales_bill.save()

        return sales_bill




class ProductBillItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)


    class Meta:
        model = ProductBillItem
        fields = ['product', 'product_name', 'quantity', 'unit_price', 'location']


    def get_product_name(self, obj):
        return obj.product.name




class ProductBillSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    items = ProductBillItemSerializer(many=True, read_only=True)

    class Meta:
        model = ProductBill
        fields = ['id', 'currency', 'discount', 'location', 'created_at', 'customer', 'items', 'total_price', 'status']