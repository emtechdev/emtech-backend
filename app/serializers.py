from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, SubCategory, Product, Pricing, ProductSpesfication, UserProfile, File, Image, PurchaseBill , PurchaseBillItem, SalesBill, SalesBillItem, ProductBill , ProductBillItem
from django.db import transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

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

    class Meta:
        model = Product
        fields = ('id', 'subcategory', 'file_url', 'file', 'name',
                  'image', 'description', 'series',
                  'manfacturer', 'origin', 'eg_stock',
                  'ae_stock', 'tr_stock')

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.file.url
        return None
    

class PricingSerializer(serializers.ModelSerializer):
    eg_final_price_usd = serializers.ReadOnlyField()
    eg_final_price_usd_egp = serializers.ReadOnlyField()
    eg_final_price_usd_eur = serializers.ReadOnlyField()
    eg_final_price_usd_tr = serializers.ReadOnlyField()
    eg_final_price_usd_rs = serializers.ReadOnlyField()
    eg_final_price_usd_ae = serializers.ReadOnlyField()
    eg_final_price_usd_strlini = serializers.ReadOnlyField()
    
    eg_final_price_eur = serializers.ReadOnlyField()
    eg_final_price_eur_usd = serializers.ReadOnlyField()
    eg_final_price_eur_egp = serializers.ReadOnlyField()
    eg_final_price_eur_tr = serializers.ReadOnlyField()
    eg_final_price_eur_rs = serializers.ReadOnlyField()
    eg_final_price_eur_ae = serializers.ReadOnlyField()
    eg_final_price_eur_strlini = serializers.ReadOnlyField()
    
    ae_final_price_usd = serializers.ReadOnlyField()
    ae_final_price_usd_egp = serializers.ReadOnlyField()
    ae_final_price_usd_eur = serializers.ReadOnlyField()
    ae_final_price_usd_tr = serializers.ReadOnlyField()
    ae_final_price_usd_rs = serializers.ReadOnlyField()
    ae_final_price_usd_ae = serializers.ReadOnlyField()
    ae_final_price_usd_strlini = serializers.ReadOnlyField()
    
    ae_final_price_eur = serializers.ReadOnlyField()
    ae_final_price_eur_usd = serializers.ReadOnlyField()
    ae_final_price_eur_egp = serializers.ReadOnlyField()
    ae_final_price_eur_tr = serializers.ReadOnlyField()
    ae_final_price_eur_rs = serializers.ReadOnlyField()
    ae_final_price_eur_ae = serializers.ReadOnlyField()
    ae_final_price_eur_strlini = serializers.ReadOnlyField()
    
    tr_final_price_usd = serializers.ReadOnlyField()
    tr_final_price_usd_egp = serializers.ReadOnlyField()
    tr_final_price_usd_eur = serializers.ReadOnlyField()
    tr_final_price_usd_tr = serializers.ReadOnlyField()
    tr_final_price_usd_rs = serializers.ReadOnlyField()
    tr_final_price_usd_ae = serializers.ReadOnlyField()
    tr_final_price_usd_strlini = serializers.ReadOnlyField()
    
    tr_final_price_eur = serializers.ReadOnlyField()
    tr_final_price_eur_usd = serializers.ReadOnlyField()
    tr_final_price_eur_egp = serializers.ReadOnlyField()
    tr_final_price_eur_tr = serializers.ReadOnlyField()
    tr_final_price_eur_rs = serializers.ReadOnlyField()
    tr_final_price_eur_ae = serializers.ReadOnlyField()
    tr_final_price_eur_strlini = serializers.ReadOnlyField()
    
    class Meta:
        model = Pricing
        fields = (
           'id', 'product', 'time',
            'eg_buy_price', 'eg_cost', 'eg_profit',
            'ae_buy_price', 'ae_cost', 'ae_profit',
            'tr_buy_price', 'tr_cost', 'tr_profit',
            'usd_to_egp', 'usd_to_eur', 'usd_to_tr', 'usd_to_rs', 'usd_to_ae', 'usd_to_strlini',
            'eur_to_egp', 'eur_to_usd', 'eur_to_tr', 'eur_to_rs', 'eur_to_ae', 'eur_to_strlini',
            'eg_final_price_usd', 'eg_final_price_usd_egp', 'eg_final_price_usd_eur',
            'eg_final_price_usd_tr', 'eg_final_price_usd_rs', 'eg_final_price_usd_ae',
            'eg_final_price_usd_strlini', 'eg_final_price_eur', 'eg_final_price_eur_usd',
            'eg_final_price_eur_egp', 'eg_final_price_eur_tr', 'eg_final_price_eur_rs',
            'eg_final_price_eur_ae', 'eg_final_price_eur_strlini', 'ae_final_price_usd',
            'ae_final_price_usd_egp', 'ae_final_price_usd_eur', 'ae_final_price_usd_tr',
            'ae_final_price_usd_rs', 'ae_final_price_usd_ae', 'ae_final_price_usd_strlini',
            'ae_final_price_eur', 'ae_final_price_eur_usd', 'ae_final_price_eur_egp',
            'ae_final_price_eur_tr', 'ae_final_price_eur_rs', 'ae_final_price_eur_ae',
            'ae_final_price_eur_strlini', 'tr_final_price_usd', 'tr_final_price_usd_egp',
            'tr_final_price_usd_eur', 'tr_final_price_usd_tr', 'tr_final_price_usd_rs',
            'tr_final_price_usd_ae', 'tr_final_price_usd_strlini', 'tr_final_price_eur',
            'tr_final_price_eur_usd', 'tr_final_price_eur_egp', 'tr_final_price_eur_tr',
            'tr_final_price_eur_rs', 'tr_final_price_eur_ae', 'tr_final_price_eur_strlini'
        )


class ProductSpesficationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpesfication
        fields = '__all__'

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
    

class ProductSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    image = ImageSerializer()

    class Meta:
        model = Product
        fields = ('id', 'subcategory', 'file_url', 'file', 'name',
                  'image', 'description', 'series',
                  'manfacturer', 'origin', 'eg_stock',
                  'ae_stock', 'tr_stock')

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.file.url
        return None
    

class PurchaseBillItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = PurchaseBillItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'location']

class PurchaseBillSerializer(serializers.ModelSerializer):
    items = PurchaseBillItemSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseBill
        fields = ['id', 'name', 'purchase_date', 'total_price', 'items']




class SalesBillItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SalesBillItem
        fields = ['id', 'product',  'quantity', 'location']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)
        validated_data['product'] = product
        return super().create(validated_data)



class SalesBillSerializer(serializers.ModelSerializer):
    items = SalesBillItemSerializer(many=True, read_only=True, source='salesbillitem_set')

    class Meta:
        model = SalesBill
        fields = ['id', 'name', 'sales_date', 'total_price', 'items']

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
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductBillItem
        fields = ['product', 'product_name', 'quantity', 'unit_price', 'location']

    def get_product_name(self, obj):
        return obj.product.name

class ProductBillSerializer(serializers.ModelSerializer):
    items = ProductBillItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    product_names = serializers.SerializerMethodField()

    class Meta:
        model = ProductBill
        fields = ['id', 'currency', 'discount', 'location', 'created_at', 'items', 'total_price', 'product_names']

    def get_total_price(self, obj):
        # Call the get_total_price method from ProductBill model
        return obj.get_total_price()

    def get_product_names(self, obj):
        # Create a list of product names from the bill items
        return [item.product.name for item in obj.items.all()]