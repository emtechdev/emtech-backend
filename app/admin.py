from django.contrib import admin
from .models import(Category, SubCategory, Product, Pricing,
                     ProductSpesfication, File, UserProfile,
                       Image, PurchaseBill, PurchaseBillItem,
                         SalesBill, SalesBillItem, ProductBill,
                           ProductBillItem, Specification,
                             ProductSpesfication)




admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(File)
admin.site.register(UserProfile)
admin.site.register(Image)
admin.site.register(Pricing)
admin.site.register(ProductSpesfication)
admin.site.register(PurchaseBill)
admin.site.register(PurchaseBillItem)
admin.site.register(SalesBill)
admin.site.register(SalesBillItem)
admin.site.register(ProductBill)
admin.site.register(ProductBillItem)
admin.site.register(Specification)