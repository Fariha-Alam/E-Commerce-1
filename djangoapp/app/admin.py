from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
  Customer,
  Product,
  Cart,
  OrderPlaced,
  NewCollection,
  DiscountProduct,
  Review,
  Wishlist

)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id','user','name','email','mobile','locality','city','zipcode','state']
@admin.register(Product)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id','title','selling_price','discounted_price','brand','description','description_2','category','product_image']
@admin.register(Cart)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id','user','product','quantity','purchased']
@admin.register(OrderPlaced)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id','user','product','product_info','quantity','ordered_date','ordered','payment_Id','order_Id','status']


    def product_info(self,obj):
        link=reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    
@admin.register(NewCollection)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id','title','selling_price','description','category','product_image']
@admin.register(DiscountProduct)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id','title','selling_price','discounted_price','description','category','product_image']    

@admin.register(Review)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['product','user','rating','comment','created_at']
    
@admin.register(Wishlist)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['user','product']
admin.site.site_header = "Eshop"
# Register your models here.
