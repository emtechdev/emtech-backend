from django.contrib import admin
from .models import Category, SubCategory, Product, Pricing, ProductSpesfication, File, UserProfile, Image




admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(File)
admin.site.register(UserProfile)
admin.site.register(Image)