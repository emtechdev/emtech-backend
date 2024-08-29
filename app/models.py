from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('Admin', 'Admin'),
        ('Engineer', 'Engineer'),
        ('Employee', 'Employee'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kind = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='Employee')

    def __str__(self):
        return f"{self.user.username} ({self.kind})"
    

    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class File(models.Model):
    file = models.FileField()
    
    def __str__(self):
        return self.file.url


class Image(models.Model):
    image = models.ImageField()
    
    def __str__(self):
        return self.image.url



class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    file_link = models.URLField(max_length=500, null=True, blank=True)  
    name = models.CharField(max_length=255, unique=True)
    series = models.CharField(max_length=255)
    manfacturer = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    eg_stock = models.IntegerField()
    ae_stock = models.IntegerField()
    tr_stock = models.IntegerField()


    
    def __str__(self):
        return self.name
    


    
class Pricing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, null= True, blank=True)
    eg_buy_price = models.IntegerField()
    eg_cost = models.IntegerField()
    eg_profit = models.IntegerField()
    ae_buy_price = models.IntegerField()
    ae_cost = models.IntegerField()
    ae_profit = models.IntegerField()
    tr_buy_price = models.IntegerField()
    tr_cost = models.IntegerField()
    tr_profit = models.IntegerField()

    @property
    def eg_final_price(self):
        return self.eg_buy_price * self.eg_profit * self.eg_cost

    @property
    def ae_final_price(self):
        return self.ae_buy_price * self.ae_profit * self.ae_cost
    
    @property
    def tr_final_price(self):
        return self.tr_buy_price * self.tr_profit * self.tr_cost
    


class ProductSpesfication(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name