from rest_framework import  viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from rest_framework import status
from .filters import ProductFilter
from django.db.models import Q
from .permissions import IsAdminOrEngineer
from rest_framework.exceptions import MethodNotAllowed
from django.db import transaction


from .models import (Category, SubCategory, Product, Pricing, ProductSpesfication,
                      UserProfile, File, Image, PurchaseBill, PurchaseBillItem,
                        SalesBill, SalesBillItem, ProductBill, ProductBillItem,
                          Specification, ProductSpesfication, Trader, Customer)


from .serializers import (CategorySerializer, SubCategorySerializer,
                           ProductSerializer, PricingSerializer,
                             ProductSpesficationSerializer , UserSerializer,
                               FileSerializer, ImageSerializer,
                                 PurchaseBillSerializer, PurchaseBillItemSerializer,
                                   SalesBillSerializer, SalesBillItemSerializer, ProductBillItemSerializer,
                                     ProductBillSerializer, SpecificationSerializer,
                                       ProductSpesficationSerializer, TraderSerializer, CustomerSerializer)


from rest_framework.decorators import api_view
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ProductFilter
from django_filters import rest_framework as filters

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
    permission_classes = [IsAdminOrEngineer]  

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to prevent deletion
        raise MethodNotAllowed('DELETE')

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
    permission_classes = [IsAdminOrEngineer]  


    @action(detail=True, methods=['get'], url_name='filter_products', url_path='filter_products')
    def filter_products(self, request, pk=None):
        # Get the subcategory based on the ID from the URL
        try:
            subcategory = SubCategory.objects.get(id=pk)
        except SubCategory.DoesNotExist:
            return Response({"error": "SubCategory not found"}, status=404)

        # Get the query params and start filtering the products
        queryset = Product.objects.filter(subcategory=subcategory)
        params = self.request.query_params

        # Filter by static fields with exact matching
        for key, value in params.items():
            if key in ['name', 'series', 'manfacturer', 'origin', 'description']:
                queryset = queryset.filter(**{f'{key}__exact': value})
            elif key in ['eg_stock', 'ae_stock', 'tr_stock']:
                try:
                    queryset = queryset.filter(**{f'{key}': int(value)})
                except ValueError:
                    return Response({"error": f"Invalid value for {key}"}, status=400)
            else:
                # Dynamic filters for specifications
                queryset = queryset.filter(
                    Q(specifications__specification__name__iexact=key) &
                    Q(specifications__value__iexact=value)
                ).distinct()

        # Serialize the filtered queryset
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    


    @action(detail=True, methods=['get'], url_name='filter_options', url_path='filter_options')
    def filter_options(self, request, pk=None):
        try:
            subcategory = SubCategory.objects.get(id=pk)
            specifications = subcategory.specifications.all()

            # Prepare the filter data
            filter_data = {
                'name': list(Product.objects.filter(subcategory=subcategory).values_list('name', flat=True).distinct()),
                'series': list(Product.objects.filter(subcategory=subcategory).values_list('series', flat=True).distinct()),
                'manfacturer': list(Product.objects.filter(subcategory=subcategory).values_list('manfacturer', flat=True).distinct()),
                'origin': list(Product.objects.filter(subcategory=subcategory).values_list('origin', flat=True).distinct()),
            }

            # Create a dictionary for the specification names and their corresponding values
            spec_data = {}
            for spec in specifications:
                spec_values = ProductSpesfication.objects.filter(
                    Q(product__subcategory=subcategory) & 
                    Q(specification=spec)
                ).values_list('value', flat=True).distinct()

                spec_data[spec.name] = list(spec_values)

            filter_data['specifications'] = spec_data

            return Response(filter_data)
        
        except SubCategory.DoesNotExist:
            return Response({"error": "SubCategory not found"}, status=404)


    @action(detail=True, methods=['get'], url_path='specifications')
    def specifications(self, request, pk=None):
        # Get the subcategory by its primary key
        subcategory = self.get_object()

        # Get all specifications for that subcategory
        specifications = subcategory.specifications.all()

        # Serialize the specifications
        specification_data = [

            { 
                "id": spec.id,
                "name": spec.name,
                "value": spec.value
            } for spec in specifications
        ]

        return Response(specification_data)
    

    @action(detail=True, methods=['post'], url_name='add_specification', url_path='add_specification')
    def add_specification(self, request, pk=None):
        subcategory = self.get_object()  # Get the specific subcategory by ID
        spec_data = request.data

        # Validate that both name and value are provided
        name = spec_data.get('name')
        value = spec_data.get('value')

        if not name or not value:
            return Response({'error': 'Specification name and value are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get the specification
        specification, created = Specification.objects.get_or_create(name=name, value=value)

        # Add the specification to the subcategory
        subcategory.specifications.add(specification)

        return Response({
            'success': 'Specification added to subcategory.',
            'specification': SpecificationSerializer(specification).data
        }, status=status.HTTP_201_CREATED)


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
        file = request.FILES.get('file')  # Get the uploaded file
        manfacturer = request.data.get('manfacturer')
        origin = request.data.get('origin')
        description = request.data.get('description')
        image = request.FILES.get('image')  # Get the uploaded image
        eg_stock = request.data.get('eg_stock')
        ae_stock = request.data.get('ae_stock')
        tr_stock = request.data.get('tr_stock')

        if not name:
            return Response({'error': 'Name is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        file_instance = None
        if file:
            file_instance = File.objects.create(file=file)

        image_instance = None
        if image:
            image_instance = image

        try:
            product = Product.objects.create(
                name=name,
                series=series,
                file=file_instance, 
                manfacturer=manfacturer,
                origin=origin,
                description=description,
                image=image_instance, 
                eg_stock=eg_stock,
                ae_stock=ae_stock,
                tr_stock=tr_stock,
                subcategory=subcategory
            )
        except Exception as e:
            return Response({'error': f'Failed to create Product: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        product_data = ProductSerializer(product).data

        return Response(product_data, status=status.HTTP_201_CREATED)



class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related('specifications__specification')
    serializer_class = ProductSerializer
    paginate_by = 10
    permission_classes = [IsAdminOrEngineer]  




    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        # Filter by static fields with exact matching
        for key, value in params.items():
            if key in ['name', 'series', 'manfacturer', 'origin', 'description']:
                queryset = queryset.filter(**{f'{key}__exact': value})
            elif key in ['eg_stock', 'ae_stock', 'tr_stock']:
                # Ensure numeric fields are handled correctly
                queryset = queryset.filter(**{f'{key}': int(value)})
            elif key == 'category':
                queryset = queryset.filter(subcategory__category__name__exact=value)
            elif key == 'subcategory':
                queryset = queryset.filter(subcategory__name__exact=value)
            else:
                # Handle dynamic filters for specifications using Q objects
                queryset = queryset.filter(
                    Q(specifications__specification__name__iexact=key) &
                    Q(specifications__value__iexact=value)
                ).distinct()

        return queryset
    



    @action(detail=False, methods=['get'], url_name='filter_options', url_path='filter_options')
    def filter_options(self, request):
        filter_data = {
            'name': list(Product.objects.values_list('name', flat=True).distinct()),
            'series': list(Product.objects.values_list('series', flat=True).distinct()),
            'manfacturer': list(Product.objects.values_list('manfacturer', flat=True).distinct()),
            'origin': list(Product.objects.values_list('origin', flat=True).distinct()),
            'category': list(SubCategory.objects.values_list('category__name', flat=True).distinct()),
            'subcategory': list(SubCategory.objects.values_list('name', flat=True).distinct()),
        }

        # Add specification names and values
        specifications = Specification.objects.values_list('name', flat=True).distinct()
        for spec in specifications:
            filter_data[spec] = list(ProductSpesfication.objects.filter(specification__name=spec).values_list('value', flat=True).distinct())

        return Response(filter_data)


    
    @action(detail=True, methods=['post'])
    def add_selected_file(self, request, pk=None, url_name='add_selected_file', url_path='add_selected_file'):
        product = self.get_object()
        file_id = request.data.get('file_id')
        
        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        
        product.file = file
        product.save()
        return Response({'status': 'file added'}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'], url_name='add_file', url_path='add_file')
    def add_file(self, request, pk=None):
        product = self.get_object()
        file_serializer = FileSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file = file_serializer.save()
            product.file = file
            product.save()
            return Response({'status': 'file added'}, status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


    @action(detail=True, methods=['post'])
    def add_selected_image(self, request, pk=None, url_name='add_selected_image', url_path='add_selected_image'):
        product = self.get_object()
        image_id = request.data.get('image_id')
        
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
        
        product.image = image
        product.save()
        return Response({'status': 'image added'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_name='add_image', url_path='add_image')
    def add_image(self, request, pk=None):
        product = self.get_object()
        image_serializer = ImageSerializer(data=request.data)
        
        if image_serializer.is_valid():
            image = image_serializer.save()
            product.image = image
            product.save()
            return Response({'status': 'image added'}, status=status.HTTP_200_OK)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'error': f'Validation error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
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

        location = request.query_params.get('location', 'EG')  # Get location from query parameters
        currency = request.query_params.get('currency', 'USD')  # Get currency from query parameters

        pricing = Pricing.objects.filter(product=product).prefetch_related('product')
        serializer = PricingSerializer(pricing, many=True, context={'location': location, 'currency': currency})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='specifications')
    def list_specifications(self, request, pk=None):
        """List all specifications for the subcategory related to a specific product."""
        product = self.get_object()
        subcategory = product.subcategory
        
        # Retrieve all specifications related to the subcategory
        specifications = subcategory.specifications.all()
        
        serializer = SpecificationSerializer(specifications, many=True)
        return Response(serializer.data)






    @action(detail=True, methods=['post'], url_path='add_specification')
    def add_specification(self, request, pk=None):
        product = self.get_object()
        specification_id = request.data.get('specification_id')
        value = request.data.get('value')

        try:
            specification = Specification.objects.get(id=specification_id, subcategory=product.subcategory)
            
            product_specification, created = ProductSpesfication.objects.get_or_create(
                product=product,
                specification=specification,
                defaults={'value': value}
            )

            if not created:
                product_specification.value = value
                product_specification.save()

            return Response({'success': 'Specification added/updated successfully.'}, status=status.HTTP_200_OK)
        except Specification.DoesNotExist:
            return Response({'error': 'Specification does not exist for this subcategory.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


    @action(detail=True, methods=['get'], url_path='list_product_specifications')
    def list_product_specifications(self, request, pk=None):
        """List all specifications for a product along with their values."""
        product = self.get_object()

        # Fetch all ProductSpesfication entries related to the product
        product_specifications = ProductSpesfication.objects.filter(product=product)

        # Create a dictionary to hold specifications and their associated values
        specifications_data = {}
        for ps in product_specifications:
            spec_name = ps.specification.name
            if spec_name not in specifications_data:
                specifications_data[spec_name] = {
                    'specification_id': ps.specification.id,
                    'specification_value': ps.specification.value,
                    'product_specifications': []
                }
            specifications_data[spec_name]['product_specifications'].append({
                'id': ps.id,
                'value': ps.value
            })

        # Convert the dictionary to a list of dictionaries
        data = [
            {
                'specification_id': spec_data['specification_id'],
                'name': spec_name,
                'value': spec_data['specification_value'],
                'product_specifications': spec_data['product_specifications']
            }
            for spec_name, spec_data in specifications_data.items()
        ]

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='add_product_specification')
    def add_product_specification(self, request, pk=None):
        """Add a new specification to a product."""
        product = self.get_object()
        specification_id = request.data.get('specification_id')
        value = request.data.get('value')

        if not specification_id or not value:
            return Response({'error': 'Specification ID and value are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            specification = Specification.objects.get(id=specification_id)
        except Specification.DoesNotExist:
            return Response({'error': 'Specification not found.'}, status=status.HTTP_404_NOT_FOUND)

        product_specification = ProductSpesfication.objects.create(
            product=product,
            specification=specification,
            value=value
        )

        return Response({'success': f'Specification {specification.name} added to product {product.name} with value {value}.'}, status=status.HTTP_201_CREATED)



class PricingViewset(viewsets.ModelViewSet):
    queryset = Pricing.objects.all().prefetch_related('product')
    serializer_class = PricingSerializer
    paginate_by = 10
    permission_classes = [IsAdminOrEngineer]  

class ProductSpesficationViewset(viewsets.ModelViewSet):
    queryset = ProductSpesfication.objects.all().prefetch_related('product')
    serializer_class = ProductSpesficationSerializer
    permission_classes = [IsAdminOrEngineer]  


class FileViewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser] 
    permission_classes = [IsAdminOrEngineer]  


class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser, FormParser] 
    permission_classes = [IsAdminOrEngineer]  




@api_view(['POST'])
def update_pricing_with_conversion(request):
    conversion_rates = request.data

    # Validate only the fields you need for conversion, based on your Pricing model
    required_fields = [
        'usd_to_egp', 'usd_to_eur', 'usd_to_tr', 'usd_to_rs', 'usd_to_ae', 'usd_to_strlini'
    ]
    
    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in conversion_rates]
    if missing_fields:
        return Response({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    # Check for invalid values (non-numeric)
    invalid_fields = [field for field in required_fields if not isinstance(conversion_rates.get(field), (int, float))]
    if invalid_fields:
        return Response({'error': f'Invalid values for fields: {", ".join(invalid_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve all products
    products = Product.objects.all()
    created_count = 0

    for product in products:
        # Get the most recent existing pricing for the product
        existing_pricing = Pricing.objects.filter(product=product).last()

        if existing_pricing:
            try:
                # Create a new pricing instance for the product with updated conversion rates
                Pricing.objects.create(
                    product=product,
                    eg_buy_price=existing_pricing.eg_buy_price,  # Retain previous pricing values
                    eg_cost=existing_pricing.eg_cost,
                    eg_profit=existing_pricing.eg_profit,
                    ae_buy_price=existing_pricing.ae_buy_price,
                    ae_cost=existing_pricing.ae_cost,
                    ae_profit=existing_pricing.ae_profit,
                    tr_buy_price=existing_pricing.tr_buy_price,
                    tr_cost=existing_pricing.tr_cost,
                    tr_profit=existing_pricing.tr_profit,
                    # Conversion rates provided in the request
                    usd_to_egp=conversion_rates.get('usd_to_egp'),
                    usd_to_eur=conversion_rates.get('usd_to_eur'),
                    usd_to_tr=conversion_rates.get('usd_to_tr'),
                    usd_to_rs=conversion_rates.get('usd_to_rs'),
                    usd_to_ae=conversion_rates.get('usd_to_ae'),
                    usd_to_strlini=conversion_rates.get('usd_to_strlini')
                )
                created_count += 1
            except Exception as e:
                return Response({'error': f'Failed to create pricing for product {product.name}: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Return response based on how many products were updated
    if created_count == 0:
        return Response({'error': 'No existing pricing data found for any products.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'success': f'New pricing added for {created_count} products successfully.'}, status=status.HTTP_201_CREATED)




class PurchaseBillViewSet(viewsets.ModelViewSet):
    queryset = PurchaseBill.objects.all().prefetch_related('products')
    serializer_class = PurchaseBillSerializer
    paginate_by = 10

    
    def create(self, request, *args, **kwargs):
        data = request.data
        items_data = data.pop('items', [])
        trader_id = data.get('trader')

        with transaction.atomic():
            try:
                # Ensure the trader exists
                trader = Trader.objects.get(id=trader_id)

                # Create the purchase bill with a default total_price (to be updated later)
                purchase_bill = PurchaseBill.objects.create(
                    name=data.get('name'),
                    trader=trader,
                    total_price=0  # Set default value for total_price
                )

                # Get all the product IDs and fetch them
                product_ids = [item['product']['id'] for item in items_data]
                products = Product.objects.filter(id__in=product_ids)

                if len(products) != len(product_ids):
                    return Response({'error': 'One or more products not found.'}, status=status.HTTP_400_BAD_REQUEST)

                # Create PurchaseBillItem for each item
                for item_data in items_data:
                    product = products.get(id=item_data['product']['id'])
                    PurchaseBillItem.objects.create(
                        purchase_bill=purchase_bill,
                        product=product,
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price'],
                        location=item_data['location']
                    )

                # Calculate and update the total price
                purchase_bill.total_price = sum(item['quantity'] * item['unit_price'] for item in items_data)
                purchase_bill.save()

            except Trader.DoesNotExist:
                return Response({'error': 'Trader not found.'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return the created purchase bill data
        serializer = self.get_serializer(purchase_bill)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SalesBillViewSet(viewsets.ModelViewSet):
    queryset = SalesBill.objects.all().prefetch_related('products')
    serializer_class = SalesBillSerializer
    paginate_by = 10

    def create(self, request, *args, **kwargs):
        data = request.data
        items_data = data.pop('items', [])
        customer_id = data.get('customer_id')

        # Validate customer
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            customer = None

        # Initialize the SalesBill instance
        sales_bill = SalesBill(customer=customer, **data)
        sales_bill.total_price = 0

        errors = []

        # Save the SalesBill instance
        try:
            sales_bill.save()
        except Exception as e:
            return Response({'error': f'Failed to create SalesBill: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        for item_data in items_data:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity')
            location = item_data.get('location')
            unit_price = item_data.get('unit_price', 0)

            try:
                product = Product.objects.get(id=product_id)

                # Create the SalesBillItem without adjusting stock
                SalesBillItem.objects.create(
                    sales_bill=sales_bill,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    location=location
                )

                # Update total price
                sales_bill.total_price += quantity * unit_price

            except Product.DoesNotExist:
                errors.append(f"Product not found for ID {product_id}")
            except ValueError as e:
                errors.append(str(e))

        # Handle errors if any
        if errors:
            sales_bill.delete()
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated total_price
        sales_bill.save()

        serializer = self.get_serializer(sales_bill)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def adjust_stock(self, request):
        """
        Adjust stock based on the items in the SalesBill.
        """
        sales_bill_id = request.data.get('sales_bill_id')
        location = request.data.get('location')  # Optional, in case stock is location-specific

        # Validate input
        if not sales_bill_id:
            return Response({'error': 'SalesBill ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the SalesBill
        try:
            sales_bill = SalesBill.objects.get(id=sales_bill_id)
        except SalesBill.DoesNotExist:
            return Response({'error': 'SalesBill not found'}, status=status.HTTP_404_NOT_FOUND)

        errors = []

        # Use the correct related name to access SalesBillItems
        for item in sales_bill.items.all():  # If 'items' is not the related name, use 'salesbillitem_set'
            try:
                product = Product.objects.get(id=item.product.id)
                product.adjust_stock(item.quantity, location or item.location)  # Adjust stock based on location
            except Product.DoesNotExist:
                errors.append(f'Product not found for ID {item.product.id}')
            except ValueError as e:
                errors.append(str(e))

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': f'Stock adjusted successfully for SalesBill {sales_bill_id}'}, status=status.HTTP_200_OK)



class ProductBillViewSet(viewsets.ModelViewSet):
    queryset = ProductBill.objects.all()
    serializer_class = ProductBillSerializer
    paginate_by = 10

    @action(detail=False, methods=['post'])
    def create_with_products(self, request):
        data = request.data
        currency = data.get('currency')
        discount = data.get('discount', 0)
        location = data.get('location')
        products = data.get('products', [])
        customer_id = data.get('customer_id')

        # Validate customer
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Start a transaction to ensure atomicity
        with transaction.atomic():
            # Create ProductBill instance
            product_bill = ProductBill(currency=currency, discount=discount, location=location, customer=customer)
            product_bill.save()  # Save to get primary key
            print(f"ProductBill saved with ID: {product_bill.id}")

            total_amount = 0
            errors = []

            # Process products
            for item in products:
                product_id = item.get('product_id')
                quantity = item.get('quantity')

                # Get the product and check stock
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    errors.append(f'Product not found for ID {product_id}')
                    continue

                # Check stock availability
                available_stock = self.get_available_stock(product, location)
                if quantity > available_stock:
                    errors.append(f'Insufficient stock for product {product_id}. Available: {available_stock}, Requested: {quantity}')
                    continue

                # Get the latest pricing for the product
                try:
                    pricing = Pricing.objects.filter(product_id=product_id).latest('time')
                except Pricing.DoesNotExist:
                    errors.append(f'Pricing not found for product {product_id}')
                    continue

                # Calculate the unit price based on currency
                try:
                    unit_price = pricing.get_final_price(location, currency)
                except ValueError:
                    errors.append(f'Invalid location or currency for product {product_id}')
                    continue

                # Calculate total amount
                total_amount += unit_price * quantity

                # Create ProductBillItem instance
                ProductBillItem.objects.create(
                    product_bill=product_bill,
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=unit_price,
                    location=location
                )

            if errors:
                # If there were errors, roll back the creation of ProductBill
                product_bill.delete()
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            # Apply discount and save total price
            total_amount = product_bill.apply_discount(total_amount)
            product_bill.total_price = total_amount
            product_bill.save()  # Save total_price after applying discount

            serializer = self.get_serializer(product_bill)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_available_stock(self, product, location):
        """ Return available stock based on location. """
        if location == 'EG':
            return product.eg_stock
        elif location == 'AE':
            return product.ae_stock
        elif location == 'TR':
            return product.tr_stock
        else:
            raise ValueError('Invalid location')
        
    @action(detail=False, methods=['post'])
    def adjust_stock(self, request):
        """
        Adjust stock based on a given ProductBill ID.
        """
        product_bill_id = request.data.get('product_bill_id')
        location = request.data.get('location')  # Optional, if stock is location-specific

        # Validate input
        if not product_bill_id:
            return Response({'error': 'ProductBill ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the ProductBill
        try:
            product_bill = ProductBill.objects.get(id=product_bill_id)
        except ProductBill.DoesNotExist:
            return Response({'error': 'ProductBill not found'}, status=status.HTTP_404_NOT_FOUND)

        errors = []

        # Adjust stock for each ProductBillItem
        for item in product_bill.items.all():  # Assuming there's a related_name `items` on ProductBillItem
            try:
                product = Product.objects.get(id=item.product.id)
                product.adjust_stock(item.quantity, location or item.location)  # Adjust stock based on quantity and location
            except Product.DoesNotExist:
                errors.append(f'Product not found for ID {item.product.id}')
            except ValueError as e:
                errors.append(str(e))

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': f'Stock adjusted successfully for ProductBill {product_bill_id}'}, status=status.HTTP_200_OK)



class SpesficationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer


class TraderViewset(viewsets.ModelViewSet):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer



class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

















































































# @api_view(['POST'])
# def update_pricing_with_conversion(request):
#     # Get the conversion rates from the request
#     conversion_rates = request.data

#     # Validate required fields
#     required_fields = [
#         'usd_to_egp', 'usd_to_eur', 'usd_to_tr', 'usd_to_rs', 'usd_to_ae', 'usd_to_strlini',
#         'eur_to_egp', 'eur_to_usd', 'eur_to_tr', 'eur_to_rs', 'eur_to_ae', 'eur_to_strlini'
#     ]
#     missing_fields = [field for field in required_fields if field not in conversion_rates]
#     if missing_fields:
#         return Response({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

#     invalid_fields = [field for field in required_fields if not isinstance(conversion_rates.get(field), (int, float))]
#     if invalid_fields:
#         return Response({'error': f'Invalid values for fields: {", ".join(invalid_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

#     # Retrieve all products
#     products = Product.objects.all()

#     for product in products:
#         # Check if there is existing pricing for the product
#         existing_pricing = Pricing.objects.filter(product=product).first()
        
#         if existing_pricing:
#             # If existing pricing is found, create a new pricing entry with updated conversion rates
#             try:
#                 Pricing.objects.create(
#                     product=product,
#                     eg_buy_price=existing_pricing.eg_buy_price,
#                     eg_cost=existing_pricing.eg_cost,
#                     eg_profit=existing_pricing.eg_profit,
#                     ae_buy_price=existing_pricing.ae_buy_price,
#                     ae_cost=existing_pricing.ae_cost,
#                     ae_profit=existing_pricing.ae_profit,
#                     tr_buy_price=existing_pricing.tr_buy_price,
#                     tr_cost=existing_pricing.tr_cost,
#                     tr_profit=existing_pricing.tr_profit,
#                     usd_to_egp=conversion_rates.get('usd_to_egp'),
#                     usd_to_eur=conversion_rates.get('usd_to_eur'),
#                     usd_to_tr=conversion_rates.get('usd_to_tr'),
#                     usd_to_rs=conversion_rates.get('usd_to_rs'),
#                     usd_to_ae=conversion_rates.get('usd_to_ae'),
#                     usd_to_strlini=conversion_rates.get('usd_to_strlini'),
#                     eur_to_egp=conversion_rates.get('eur_to_egp'),
#                     eur_to_usd=conversion_rates.get('eur_to_usd'),
#                     eur_to_tr=conversion_rates.get('eur_to_tr'),
#                     eur_to_rs=conversion_rates.get('eur_to_rs'),
#                     eur_to_ae=conversion_rates.get('eur_to_ae'),
#                     eur_to_strlini=conversion_rates.get('eur_to_strlini')
#                 )
#             except Exception as e:
#                 return Response({'error': f'Failed to create pricing for product {product.id}: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             # If no existing pricing is found, handle accordingly
#             return Response({'error': f'No existing pricing data for product {product.id}'}, status=status.HTTP_404_NOT_FOUND)

#     return Response({'success': 'New pricing added for all products successfully.'}, status=status.HTTP_201_CREATED)

# class CurrencyViewset(viewsets.ModelViewSet):
#     queryset = Currency.objects.all()
#     serializer_class = CurrencySerializer

#     @action(detail=True, methods=['post'], url_name='add_value', url_path='add_value')
#     def add_value(self, request, pk=None):
#         if pk is None:
#             return Response({'error': 'Currency ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             currency = Currency.objects.get(pk=pk)
#         except Currency.DoesNotExist:
#             return Response({'error': 'Currency not found.'}, status=status.HTTP_404_NOT_FOUND)

#         value = request.data.get('value')


#         if not value:
#             return Response({'error': 'value is required and cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             currency_value = CurrencyValue.objects.create(
#                 value=value,
#                 currency=currency
#             )
#         except Exception as e:
#             return Response({'error': f'Failed to add currency_value: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response({'success': 'currency_value added successfully.'}, status=status.HTTP_201_CREATED)

    # @action(detail=True, methods=['get', 'post'], url_path='specifications')
    # def specifications(self, request, pk=None):
    #     product = self.get_object()
        
    #     if request.method == 'GET':
    #         # List all specifications for this product
    #         product_specifications = ProductSpesfication.objects.filter(product=product)
    #         serializer = ProductSpesficationSerializer(product_specifications, many=True)
    #         return Response(serializer.data)
        
    #     elif request.method == 'POST':
    #         # Add a new specification value for this product
    #         specification_id = request.data.get('specification_id')
    #         value = request.data.get('value')

    #         try:
    #             specification = Specification.objects.get(id=specification_id, subcategory=product.subcategory)
                
    #             # Create or update the ProductSpecification with the provided value
    #             product_specification, created = ProductSpesfication.objects.get_or_create(
    #                 product=product,
    #                 specification=specification,
    #                 defaults={'value': value}
    #             )

    #             if not created:
    #                 product_specification.value = value
    #                 product_specification.save()

    #             return Response({'success': 'Specification added/updated successfully.'}, status=status.HTTP_200_OK)
    #         except Specification.DoesNotExist:
    #             return Response({'error': 'Specification does not exist for this subcategory.'}, status=status.HTTP_400_BAD_REQUEST)
    #         except Exception as e:
    #             return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
