from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
STATE_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Cumilla', 'Cumilla'),
    ('Khulna', 'Khulna'),
    ('Rajshahi', 'Rajshahi'),
    ('Sylhet', 'Sylhet'),
    ('Chittagong', 'Chittagong'),
    ('Barisal', 'Barisal'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=15, default='')

    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField(null=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('C', 'Camera'),
    ('Cl', 'Cloth'),
   
    ('G', 'Grocery'),
  
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(default=0)
    brand = models.CharField(max_length=100)
    quantity=models.IntegerField(null=False,blank=False)
    description = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)

    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    product_image = models.ImageField(upload_to='productimg')
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.id)
    
NewCollection_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('C', 'Camera'),
    ('K', 'Keyboards'),
    ('Mo', 'Mouse'),
    ('D', 'Desktops'),
    ('P', 'Pendrive'),
)

class NewCollection(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    category = models.CharField(choices=NewCollection_CHOICES, max_length=10, default='M')
    product_image = models.ImageField(upload_to='new_collection_images')
    def __str__(self):
        return str(self.id)
Discount_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('C', 'Camera'),
    ('K', 'Keyboards'),
    ('Mo', 'Mouse'),
    ('D', 'Desktops'),
    ('P', 'Pendrive'),
)

class DiscountProduct(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discounted_price = models.FloatField()

    description = models.TextField()
    category = models.CharField(choices=Discount_CHOICES, max_length=10, default='M')
    product_image = models.ImageField(upload_to='discount_images')
    
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    purchased=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    @property
    def total(self):
        return self.quantity * self.product.discounted_price
   
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),  
)

class OrderPlaced(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
   
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)
    ordered_date =models.DateTimeField(auto_now_add=True)
    ordered=models.BooleanField(default=False)
    payment_Id=models.CharField(max_length=264 ,blank=True,null=True)
    order_Id=models.CharField(max_length=264 ,blank=True,null=True)
    status =models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')
    def __str__(self):
      return str(self.id)
    


class Review(models.Model):
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return self.user.username
# Create your models here.   myworld\Scripts\activate.bat
