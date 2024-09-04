from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static






router = DefaultRouter()
router.register('category', views.CategoryViewset, 'category')
router.register('subcategory', views.SubCategoryViewset, 'subcategory')
router.register('product', views.ProductViewset, 'product')
router.register('productspecfication', views.ProductSpesficationViewset, 'productspecfication')
router.register('product_pricing', views.PricingViewset, 'product_pricing')
router.register('file', views.FileViewset, 'file')
router.register('image', views.ImageViewset, 'image')
router.register('purchase_bills', views.PurchaseBillViewSet)
router.register('sales_bills', views.SalesBillViewSet)
router.register('product_bills', views.ProductBillViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register),
    path('users/',views.UserListView.as_view(), name='user_list'),
    path('update_pricing_with_conversion/', views.update_pricing_with_conversion, name='update_pricing_with_conversion'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)