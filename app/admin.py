from django.contrib import admin
from .models import Category, SubCategory, Product, Pricing, ProductSpesfication, File, UserProfile




admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(File)
admin.site.register(UserProfile)