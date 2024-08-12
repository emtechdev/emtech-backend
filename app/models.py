from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    series = models.CharField(max_length=255)
    manfacturer = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    eg_stock = models.IntegerField()
    ae_stock = models.IntegerField()
    tr_stock = models.IntegerField()

    def __str__(self):
        return self.name
    

class Pricing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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
    

    def __str__(self):
        return self.size
    
class ProductSpesfication(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name