from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, SubCategory, Product, Pricing, ProductSpesfication, UserProfile, File, Image


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
    

