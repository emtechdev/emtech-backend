from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter




router = DefaultRouter()
router.register('category', views.CategoryViewset, 'category')
router.register('subcategory', views.SubCategoryViewset, 'subcategory')
router.register('product', views.ProductViewset, 'product')
router.register('productspecfication', views.ProductSpesficationViewset, 'productspecfication')
router.register('product_pricing', views.PricingViewset, 'product_pricing')

urlpatterns = [
    path('', include(router.urls)),


]