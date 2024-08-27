from rest_framework import  viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from rest_framework import status
from .models import (Category, SubCategory, Product, Pricing, ProductSpesfication, UserProfile, File)
from .serializers import (CategorySerializer, SubCategorySerializer,
                           ProductSerializer, PricingSerializer,
                             ProductSpesficationSerializer , UserSerializer, FileSerializer)

from rest_framework.decorators import api_view
from rest_framework import generics
from django.contrib.auth.models import User


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def register(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        kind = request.data.get('kind')
        if kind:
            UserProfile.objects.create(user=user, kind=kind)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'], url_name='get_subcategory', url_path='get_subcategory')
    def get_subcategory(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        subcategory = SubCategory.objects.filter(category=category).prefetch_related('category')
        serializer = SubCategorySerializer(subcategory, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_name='add_subcategory', url_path='add_subcategory')
    def add_subcategory(self, request, pk=None):
        if pk is None:
            return Response({'error': 'Category ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        if not name:
            return Response({'error': 'Name is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subcategory = SubCategory.objects.create(
                name=name,
                category=category
            )
        except Exception as e:
            return Response({'error': f'Failed to create SubCategory: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': 'SubCategory added successfully.'}, status=status.HTTP_201_CREATED)


    
class SubCategoryViewset(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    @action(detail=True, methods=['get'], url_name='get_product_detail', url_path='get_product_detail')
    def get_product_detail(self, request, pk=None):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            product = Product.objects.get(pk=product_id, subcategory=subcategory)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found in this subcategory.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['get'], url_name='get_product', url_path='get_product')
    def get_product(self, request, pk=None):
        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found.'}, status=status.HTTP_404_NOT_FOUND)

        product = Product.objects.filter(subcategory=subcategory).prefetch_related('subcategory')
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_name='add_product', url_path='add_product')
    def add_product(self, request, pk=None):
        if pk is None:
            return Response({'error': 'SubCategory ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found.'}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        series = request.data.get('series')
        file = request.data.get('file')
        manfacturer = request.data.get('manfacturer')
        origin = request.data.get('origin')
        description = request.data.get('description')
        image = request.data.get('image')
        eg_stock = request.data.get('eg_stock')
        ae_stock = request.data.get('ae_stock')
        tr_stock = request.data.get('tr_stock')

        if not name:
            return Response({'error': 'Name is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.create(
                name=name,
                series=series,
                file=file,
                manfacturer=manfacturer,
                origin=origin,
                description=description,
                image=image,
                eg_stock=eg_stock,
                ae_stock=ae_stock,
                tr_stock=tr_stock,
                subcategory=subcategory
            )
        except Exception as e:
            return Response({'error': f'Failed to create Product: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': 'Product added successfully.'}, status=status.HTTP_201_CREATED)



class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    @action(detail=True, methods=['post'], url_name='add_pricing', url_path='add_pricing')
    def add_pricing(self, request, pk=None):
        if pk is None:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        pricing_data = {
            'eg_buy_price': request.data.get('eg_buy_price'),
            'eg_cost': request.data.get('eg_cost'),
            'eg_profit': request.data.get('eg_profit'),
            'ae_buy_price': request.data.get('ae_buy_price'),
            'ae_cost': request.data.get('ae_cost'),
            'ae_profit': request.data.get('ae_profit'),
            'tr_buy_price': request.data.get('tr_buy_price'),
            'tr_cost': request.data.get('tr_cost'),
            'tr_profit': request.data.get('tr_profit'),
        }

        missing_fields = [key for key, value in pricing_data.items() if value is None]
        if missing_fields:
            return Response({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

        invalid_fields = [key for key, value in pricing_data.items() if not isinstance(value, (int, float)) or value < 0]
        if invalid_fields:
            return Response({'error': f'Invalid values for fields: {", ".join(invalid_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pricing = Pricing.objects.create(product=product, **pricing_data)
        except ValidationError as e:
            print(str(e))
            return Response({'error': f'Validation error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({'error': f'Failed to create Pricing: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': 'Pricing added successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_name='get_pricing_customer', url_path='get_pricing_customer')
    def get_pricing_customer(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        pricing = Pricing.objects.filter(product=product).last()
        serializer = PricingSerializer(pricing)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_name='get_pricing', url_path='get_pricing')
    def get_pricing(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        pricing = Pricing.objects.filter(product=product).prefetch_related('product')
        serializer = PricingSerializer(pricing, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_name='get_specification', url_path='get_specification')
    def get_specification(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        specification = ProductSpesfication.objects.filter(product=product).prefetch_related('product')
        serializer = ProductSpesficationSerializer(specification, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_name='add_specification', url_path='add_specification')
    def add_specification(self, request, pk=None):
        if pk is None:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        value = request.data.get('value')

        if not name:
            return Response({'error': 'Specification name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not value:
            return Response({'error': 'Specification value is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            specification = ProductSpesfication.objects.create(
                name=name,
                value=value,
                product=product
            )
        except ValidationError as e:
            return Response({'error': f'Validation error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Failed to create specification: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': 'Specification added successfully.'}, status=status.HTTP_201_CREATED)

class PricingViewset(viewsets.ModelViewSet):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer

class ProductSpesficationViewset(viewsets.ModelViewSet):
    queryset = ProductSpesfication.objects.all()
    serializer_class = ProductSpesficationSerializer
    

class FileViewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer