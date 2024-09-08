from django.db import models
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ValidationError



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
    
class Specification(models.Model):
    name = models.CharField(max_length=255)  # Name of the specification, e.g., "Color", "Size"
    value = models.CharField(max_length=255)  # Value of the specification, e.g., "Kg", "km"

    def __str__(self):
        return f"{self.name}: {self.value}"




    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    specifications = models.ManyToManyField(Specification, related_name='subcategories', blank=True)

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

    def adjust_stock(self, quantity, location):
        print(f"Adjusting stock for product {self.id} with quantity {quantity} and location {location}")
        
        if location == 'EG':
            if self.eg_stock >= quantity:
                self.eg_stock -= quantity
            else:
                raise ValueError('Insufficient stock for EG location')
        elif location == 'AE':
            if self.ae_stock >= quantity:
                self.ae_stock -= quantity
            else:
                raise ValueError('Insufficient stock for AE location')
        elif location == 'TR':
            if self.tr_stock >= quantity:
                self.tr_stock -= quantity
            else:
                raise ValueError('Insufficient stock for TR location')
        else:
            raise ValueError('Invalid location')
        
        self.save()
        print(f"Updated stock: EG={self.eg_stock}, AE={self.ae_stock}, TR={self.tr_stock}")
        
    def __str__(self):
        return self.name
    

class ProductSpesfication(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=255)  

    def __str__(self):
        return f"{self.product.name} - {self.specification.name}: {self.value}"
    

    
class Pricing(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, null= True, blank=True)
    eg_buy_price = models.FloatField()
    eg_cost = models.FloatField()
    eg_profit = models.FloatField()
    ae_buy_price = models.FloatField()
    ae_cost = models.FloatField()
    ae_profit = models.FloatField()
    tr_buy_price = models.FloatField()
    tr_cost = models.FloatField()
    tr_profit = models.FloatField()

    usd_to_egp = models.FloatField( default=1)
    usd_to_eur = models.FloatField(default=1)
    usd_to_tr = models.FloatField(default=1)
    usd_to_rs = models.FloatField(default=1)
    usd_to_ae = models.FloatField(default=1)
    usd_to_strlini = models.FloatField(default=1)

    eur_to_egp = models.FloatField(default=1 )
    eur_to_usd = models.FloatField(default=1)
    eur_to_tr = models.FloatField(default=1)
    eur_to_rs = models.FloatField(default=1)
    eur_to_ae = models.FloatField(default=1)
    eur_to_strlini = models.FloatField(default=1)


    @property
    def eg_final_price_usd(self):
        return self.eg_buy_price * self.eg_profit * self.eg_cost

    @property
    def eg_final_price_usd(self):
        return self.eg_buy_price * self.eg_profit * self.eg_cost    

    @property
    def eg_final_price_usd_egp(self):
        return self.eg_final_price_usd * self.usd_to_egp
    
    @property
    def eg_final_price_usd_eur(self):
        return self.eg_final_price_usd * self.usd_to_eur
    
    @property
    def eg_final_price_usd_tr(self):
        return self.eg_final_price_usd * self.usd_to_tr
    
    @property
    def eg_final_price_usd_rs(self):
        return self.eg_final_price_usd * self.usd_to_rs
    
    @property
    def eg_final_price_usd_ae(self):
        return self.eg_final_price_usd * self.usd_to_ae
    
    @property 
    def eg_final_price_usd_strlini(self):
        return self.eg_final_price_usd * self.usd_to_strlini

######################################################################################

    @property
    def eg_final_price_eur(self):
        return self.eg_buy_price * self.eg_profit * self.eg_cost    


    @property
    def eg_final_price_eur_usd(self):
        return self.eg_final_price_eur * self.eur_to_usd
    
    @property
    def eg_final_price_eur_egp(self):
        return self.eg_final_price_eur * self.eur_to_egp
    
    @property
    def eg_final_price_eur_tr(self):
        return self.eg_final_price_eur * self.eur_to_tr
    
    @property
    def eg_final_price_eur_rs(self):
        return self.eg_final_price_eur * self.eur_to_rs
    
    @property
    def eg_final_price_eur_ae(self):
        return self.eg_final_price_eur * self.eur_to_ae
    
    @property 
    def eg_final_price_eur_strlini(self):
        return self.eg_final_price_eur * self.eur_to_strlini


###################################################################################

    @property
    def ae_final_price_usd(self):
        return self.ae_buy_price * self.ae_profit * self.ae_cost
    
    @property
    def ae_final_price_usd_egp(self):
        return self.ae_final_price_usd * self.usd_to_egp
    
    @property
    def ae_final_price_usd_eur(self):
        return self.ae_final_price_usd * self.usd_to_eur
    
    @property
    def ae_final_price_usd_tr(self):
        return self.ae_final_price_usd * self.usd_to_tr
    
    @property
    def ae_final_price_usd_rs(self):
        return self.ae_final_price_usd * self.usd_to_rs
    
    @property
    def ae_final_price_usd_ae(self):
        return self.ae_final_price_usd * self.usd_to_ae
    
    @property 
    def ae_final_price_usd_strlini(self):
        return self.ae_final_price_usd * self.usd_to_strlini
#################################################################################################

    @property
    def ae_final_price_eur(self):
        return self.ae_buy_price * self.ae_profit * self.ae_cost

    @property
    def ae_final_price_eur_usd(self):
        return self.ae_final_price_eur * self.eur_to_usd
    
    @property
    def ae_final_price_eur_egp(self):
        return self.ae_final_price_eur * self.eur_to_egp
    
    @property
    def ae_final_price_eur_tr(self):
        return self.ae_final_price_eur * self.eur_to_tr
    
    @property
    def ae_final_price_eur_rs(self):
        return self.ae_final_price_eur * self.eur_to_rs
    
    @property
    def ae_final_price_eur_ae(self):
        return self.ae_final_price_eur * self.eur_to_ae
    
    @property 
    def ae_final_price_eur_strlini(self):
        return self.ae_final_price_eur * self.eur_to_strlini
#################################################################################################
    @property
    def tr_final_price_usd(self):
        return self.tr_buy_price * self.tr_profit * self.tr_cost
    
    @property
    def tr_final_price_usd_egp(self):
        return self.tr_final_price_usd * self.usd_to_egp
    
    @property
    def tr_final_price_usd_eur(self):
        return self.tr_final_price_usd * self.usd_to_eur
    
    @property
    def tr_final_price_usd_tr(self):
        return self.tr_final_price_usd * self.usd_to_tr
    
    @property
    def tr_final_price_usd_rs(self):
        return self.tr_final_price_usd * self.usd_to_rs
    
    @property
    def tr_final_price_usd_ae(self):
        return self.tr_final_price_usd * self.usd_to_ae
    
    @property 
    def tr_final_price_usd_strlini(self):
        return self.tr_final_price_usd * self.usd_to_strlini
#################################################################################################

    @property
    def tr_final_price_eur(self):
        return self.tr_buy_price * self.tr_profit * self.tr_cost

    @property
    def tr_final_price_eur_usd(self):
        return self.tr_final_price_eur * self.eur_to_usd
    
    @property
    def tr_final_price_eur_egp(self):
        return self.tr_final_price_eur * self.eur_to_egp
    
    @property
    def tr_final_price_eur_tr(self):
        return self.tr_final_price_eur * self.eur_to_tr
    
    @property
    def tr_final_price_eur_rs(self):
        return self.tr_final_price_eur * self.eur_to_rs
    
    @property
    def tr_final_price_eur_ae(self):
        return self.tr_final_price_eur * self.eur_to_ae
    
    @property 
    def tr_final_price_eur_strlini(self):
        return self.tr_final_price_eur * self.eur_to_strlini

    class Meta:
        ordering = ['-time']


class Trader(models.Model):
    company_name = models.CharField(max_length=255)
    employee_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    location = models.CharField(max_length = 255)
    fax = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)

    def __str__(self):
        return self.company_name


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PurchaseBill(models.Model):
    trader = models.ForeignKey(Trader, related_name='purchase_bills', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='PurchaseBillItem')
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class PurchaseBillItem(models.Model):
    purchase_bill = models.ForeignKey(PurchaseBill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=2, choices=[('EG', 'Egypt'), ('AE', 'UAE'), ('TR', 'Turkey')])

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

            if self.location == 'EG':
                self.product.eg_stock += self.quantity
            elif self.location == 'AE':
                self.product.ae_stock += self.quantity
            elif self.location == 'TR':
                self.product.tr_stock += self.quantity
            self.product.save()


class SalesBill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='SalesBillItem')
    sales_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class SalesBillItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sales_bill = models.ForeignKey(SalesBill, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    location = models.CharField(max_length=2, choices=[('EG', 'Egypt'), ('AE', 'UAE'), ('TR', 'Turkey')])


    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Check stock availability before saving
            if self.location == 'EG':
                if self.product.eg_stock < self.quantity:
                    raise ValidationError(f"Not enough stock for product {self.product.name} in Egypt.")
                self.product.eg_stock -= self.quantity
            elif self.location == 'AE':
                if self.product.ae_stock < self.quantity:
                    raise ValidationError(f"Not enough stock for product {self.product.name} in UAE.")
                self.product.ae_stock -= self.quantity
            elif self.location == 'TR':
                if self.product.tr_stock < self.quantity:
                    raise ValidationError(f"Not enough stock for product {self.product.name} in Turkey.")
                self.product.tr_stock -= self.quantity
            
            super().save(*args, **kwargs)
            self.product.save()





class ProductBill(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('EGP', 'EGP'),
        ('TR', 'TR'),
        ('RS', 'RS'),
        ('AE', 'AE'),
        ('STR', 'STR'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    discount = models.FloatField(default=0)  # Discount as a percentage
    location = models.CharField(max_length=3, choices=[('EG', 'Egypt'), ('AE', 'UAE'), ('TR', 'Turkey')])
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Add this field

    def apply_discount(self, total_amount):
        return total_amount - (total_amount * (self.discount / 100))

    def get_total_price(self):
        total_amount = sum(item.get_total_price() for item in self.items.all())
        return self.apply_discount(total_amount)

    def get_detailed_items(self):
        return [
            {
                'product_name': item.product.name,
                'product_series': item.product.series,
                'product_origin': item.product.origin,
                'product_manufacturer': item.product.manufacturer,
                'unit_price': item.unit_price,
                'quantity': item.quantity,
                'total_price': item.get_total_price()
            }
            for item in self.items.all()
        ]


    def __str__(self):
        return str(self.total_price)
    

class ProductBillItem(models.Model):
    product_bill = models.ForeignKey(ProductBill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    location = models.CharField(max_length=50)

    def get_total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"

    def save(self, *args, **kwargs):
        # Adjust stock based on location
        self.product.adjust_stock(self.quantity, self.location)
        super().save(*args, **kwargs)


