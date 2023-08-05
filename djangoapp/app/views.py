from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from .models import Customer, Product, NewCollection, DiscountProduct, Cart, OrderPlaced,Review,Wishlist
from .forms import SignUpForm,CustomerProfileForm,PasswordChangeForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.urls import reverse
from .forms import ReviewForm
from django.utils import timezone
import json
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import requests
from sslcommerz_python.payment import SSLCSession

from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
#def home(request):
# return render(request, 'app/home.html')

class ProductView(View):
 def get(self,request):
    totalitem=0
    products = Product.objects.all()
    Mobile = Product.objects.filter(category='M')
    Laptop = Product.objects.filter(category='L')
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    context = {'products': products,'Mobile': Mobile,'Laptop': Laptop,'totalitem':totalitem}
    return render(request, 'app/home.html', context)
class MainProductView(View):
    def get(self,request):
        Mobile = Product.objects.filter(category='M')
        Laptop = Product.objects.filter(category='L')
        Camera = Product.objects.filter(category='C')
        Keyboards = Product.objects.filter(category='K')
        Mouse = Product.objects.filter(category='Mo')
        Desktops = Product.objects.filter(category='D')
        Pendrive = Product.objects.filter(category='P')

        context = {
            'Mobile': Mobile,
            'Laptop': Laptop,
            'Camera': Camera,
            'Keyboards': Keyboards,
            'Mouse': Mouse,
            'Desktops': Desktops,
            'Pendrive': Pendrive,
        }
    
        return render(request, 'app/home.html', context)

#def product_detail(request):
# return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        products = Product.objects.get(pk=pk)
        reviews = Review.objects.filter(product=products).order_by('-created_at')
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'products':products, 'reviews':reviews,'totalitem':totalitem})
class MainProductDetailView(View):
    def get(self,request,pk):
        products = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'products':products})
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)  # retrieve the Product instance
    if Cart.objects.filter(user=user, product=product).exists():
        messages.info(request, 'Product is already in your cart.')
    else:
        Cart(user=user, product=product).save()
        Wishlist.objects.filter(user=user, product=product).delete()
    return redirect( '/cart')
   
@login_required
def show_cart(request):
  totalitem=0
  if request.user.is_authenticated:
    user=request.user
    cart=Cart.objects.filter(user=user)
    print(cart)
    amount=0.0
    shipping_amount=100.0
    total=0.0
    cart_product=[p for p in Cart.objects.all() if p.user ==user]
    print(cart_product)
    totalitem=len(Cart.objects.filter(user=request.user))
    if cart_product:
            for p in cart_product:
                if p.product.discounted_price == 0:
                    tempamount = p.quantity * p.product.selling_price
                else:
                    tempamount = p.quantity * p.product.discounted_price
                amount += tempamount
                total = amount + shipping_amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'total': total, 'amount': amount,'totalitem':totalitem})

    else:
            return render(request, 'app/emptycart.html')
def plus_cart(request):
  if request.method =='GET':
   
    prod_id=request.GET['prod_id']
    print(prod_id)
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount=0.0
    shipping_amount=100.0
    total=0.0
    cart_product=[p for p in Cart.objects.all() if p.user ==request.user]
    for p in cart_product:
                if p.product.discounted_price == 0:
                    tempamount = p.quantity * p.product.selling_price
                else:
                    tempamount = p.quantity * p.product.discounted_price
                amount +=tempamount
                total=amount+shipping_amount
    data={
          'quantity':c.quantity,
          'amount':amount,
          'total':total
        }
    return JsonResponse(data)
def minus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity > 1:  # Check if quantity is greater than 1
            c.quantity -= 1
            c.save()
            disable_minus_button = False  # Enable minus button after decrement
        else:
            disable_minus_button = True  # Disable minus button when quantity is 1
        amount = 0.0
        shipping_amount = 100.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            if p.product.discounted_price == 0:
                tempamount = p.quantity * p.product.selling_price
            else:
                tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
            
        if c.quantity == 0:
            shipping_amount = 0.0

        total = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total': total,
            'disable_minus_button': disable_minus_button
        }
        return JsonResponse(data)


def remove_cart(request):
  if request.method =='GET':
   
    prod_id=request.GET['prod_id']
    print(prod_id)
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    
    c.delete()
    amount=0.0
    shipping_amount=100.0
    total=0.0
    cart_product=[p for p in Cart.objects.all() if p.user ==request.user]
    for p in cart_product:
        if p.product.discounted_price == 0:
            tempamount = p.quantity * p.product.selling_price
        else:
            tempamount = p.quantity * p.product.discounted_price
        amount += tempamount
        total = amount + shipping_amount
    data={
          
          'amount':amount,
          'total':total
        }
    return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

#def profile(request):
# return render(request, 'app/profile.html')
@login_required
def address(request):
 totalitem=0
 add=Customer.objects.filter(user=request.user)
 if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})
@login_required
def orders(request):
 totalitem=0
 op=OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))

 return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})


def mobile(request, data=None):
    totalitem=0
    mobile = None
    
    if data is None:
        mobile = Product.objects.filter(category='M')
    elif data == 'below':  
        mobile = Product.objects.filter(category='M', selling_price__lt=20000)
    elif data == 'above':  
        mobile = Product.objects.filter(category='M', selling_price__gte=20000)
    else:
        mobile = Product.objects.filter(category='M', brand=data)
    
    paginator = Paginator(mobile, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Retrieve unique brand names from the Product model
    brands = Product.objects.filter(category='M').values('brand').annotate(num_products=Count('id')).order_by('-num_products')

    if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html', {
        'page_obj': page_obj,
        'brands': brands,'totalitem':totalitem
    })


def laptop(request, data=None):
    totalitem=0
    laptop = None
    
    if data is None:
        laptop = Product.objects.filter(category='L')
    elif data == 'below':  
        laptop = Product.objects.filter(category='L', selling_price__lt=70000)
    elif data == 'above':  
        laptop = Product.objects.filter(category='L', selling_price__gte=70000)
    else:
        laptop = Product.objects.filter(category='L', brand=data)
    
    paginator = Paginator(laptop, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Retrieve unique brand names from the Product model
    brands = Product.objects.filter(category='L').values('brand').annotate(num_products=Count('id')).order_by('-num_products')

    if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html', {
        'page_obj': page_obj,
        'brands': brands,'totalitem':totalitem
    })



def camera(request, data=None):
    totalitem=0
    camera = None
    
    if data is None:
        camera = Product.objects.filter(category='C')
    elif data == 'below':  
        camera = Product.objects.filter(category='C', selling_price__lt=30000)
    elif data == 'above':  
        camera = Product.objects.filter(category='C', selling_price__gte=30000)
    else:
        camera = Product.objects.filter(category='C', brand=data)
    
    paginator = Paginator(camera, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Retrieve unique brand names from the Product model
    brands = Product.objects.filter(category='C').values('brand').annotate(num_products=Count('id')).order_by('-num_products')

    if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/camera.html', {
        'page_obj': page_obj,
        'brands': brands,'totalitem':totalitem
    })

def grocery(request, data=None):
    totalitem=0
    grocery = None
    
    if data is None:
        grocery = Product.objects.filter(category='G')
    elif data == 'below':  
        grocery = Product.objects.filter(category='G', selling_price__lt=2000)
    elif data == 'above':  
        grocery = Product.objects.filter(category='G', selling_price__gte=2000)
    else:
        grocery = Product.objects.filter(category='G', brand=data)
    
    paginator = Paginator(grocery, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Retrieve unique brand names from the Product model
    brands = Product.objects.filter(category='G').values('brand').annotate(num_products=Count('id')).order_by('-num_products')

    if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/grocery.html', {
        'page_obj': page_obj,
        'brands': brands,'totalitem':totalitem
    })

def cloth(request, data=None):
    totalitem=0
    cloth = None
    
    if data is None:
        cloth = Product.objects.filter(category='Cl')
    elif data == 'below':  
        cloth = Product.objects.filter(category='Cl', selling_price__lt=3000)
    elif data == 'above':  
        cloth = Product.objects.filter(category='Cl', selling_price__gte=3000)
    else:
        cloth = Product.objects.filter(category='Cl', brand=data)
    
    paginator = Paginator(cloth, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Retrieve unique brand names from the Product model
    brands = Product.objects.filter(category='Cl').values('brand').annotate(num_products=Count('id')).order_by('-num_products')

    if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/cloth.html', {
        'page_obj': page_obj,
        'brands': brands,'totalitem':totalitem
    })

class SearchView(View):
    def get(self, request):
        totalitem=0
        query = request.GET.get('q')
        if not query:
            return render(request, 'app/search.html', {'error': 'No search query specified'})

        products = Product.objects.filter(Q(title__icontains=query) | Q(brand__icontains=query) | Q(description__icontains=query))
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
        context = {'products': products, 'query': query,'totalitem':totalitem}
        return render(request, 'app/search.html', context)
#def login(request):
# return render(request, 'app/login.html')

#def customerregistration(request):
# return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
  def get(self,request):
   form=SignUpForm()
   return render(request,'app/customerregistration.html',{'form':form})
  def post(self,request):
   form=SignUpForm(request.POST)
   if form.is_valid():
     messages.success(request,'Congratulations. your registration complete')
     form.save()
   return render(request,'app/customerregistration.html',{'form':form})

 
@login_required  
def checkout(request):
 totalitem=0
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=100.0
 total=0.0
 cart_product=[p for p in Cart.objects.all() if p.user ==request.user]
 if cart_product:
    for p in cart_product:
                if p.product.discounted_price == 0:
                    tempamount = p.quantity * p.product.selling_price
                else:
                    tempamount = p.quantity * p.product.discounted_price
                amount +=tempamount
                total=amount+shipping_amount
               
 if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
 return render(request, 'app/checkout.html',{'add':add,'total':total,'cart_items':cart_items,'totalitem':totalitem})
@login_required
def payment_done(request):
    custid = request.POST.get('custid', '')
    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        messages.error(request, 'The selected customer does not exist. Please select a valid customer and try again.')
        return redirect('checkout')

    cart = Cart.objects.filter(user=request.user)
    orders = []
    for c in cart:
        order = OrderPlaced(user=request.user,
                            customer=customer,
                            product=c.product,
                            quantity=c.quantity)
        orders.append(order)
        order.save()

    cart.delete()
    messages.info(request, '')
    return redirect('orders')



@method_decorator(login_required,name='dispatch')
class profileView(LoginRequiredMixin, View):
    def get(self, request):
        totalitem=0
        user = request.user
        try:
            profile = Customer.objects.get(user=user)
            return redirect('profile-edit')
        except Customer.DoesNotExist:
            pass
        form = CustomerProfileForm()
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary','totalitem':totalitem})

    def post(self, request):
        totalitem=0
        user = request.user
        try:
            profile = Customer.objects.get(user=user)
            return redirect('profile-edit')
        except Customer.DoesNotExist:
            pass
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']

            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, email=email,mobile=mobile,locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.info(request, 'Congratulations, your profile has been created!')
            return redirect('profile')
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary','totalitem':totalitem})

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        totalitem=0
        user = request.user
        try:
            profile = Customer.objects.get(user=user)
            form = CustomerProfileForm(instance=profile)
        except Customer.DoesNotExist:
            messages.error(request, 'You need to create a profile before you can edit it.')
            return redirect('profile')
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile_edit.html', {'form': form,'active': 'btn-primary','totalitem':totalitem})

    def post(self, request):
        totalitem=0
        user = request.user
        try:
            profile = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            messages.error(request, 'You need to create a profile before you can edit it.')
            return redirect('profile')
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile has been updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile_edit.html', {'form': form,'totalitem':totalitem})

@login_required
def payment(request):
    # create a payment request using SSLCommerz
    store_id = 'techh6447fca78b21e'
    API_key = 'techh6447fca78b21e@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)
    status_url = request.build_absolute_uri(reverse('complete'))
    print(status_url)
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    # Retrieve customer information from the request's user object
    user = request.user
    user = Customer.objects.get(user=user)
    cart_items = Cart.objects.filter(user=request.user)
    amount=0.0
    shipping_amount=100.0
    total=0.0
    cart_product=[p for p in Cart.objects.all() if p.user ==request.user]
    if cart_product:
       for p in cart_product:
                if p.product.discounted_price == 0:
                    tempamount = p.quantity * p.product.selling_price
                else:
                    tempamount = p.quantity * p.product.discounted_price
                amount +=tempamount
                total=amount+shipping_amount
    
    if cart_product == 0:
        shipping_amount = 0
    else:
        shipping_amount = 100
  
    mypayment.set_product_integration(total_amount=Decimal(str(total)), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=Cart.objects.filter(user=request.user).count(), shipping_method='YES', product_profile='None')

    mypayment.set_customer_info(name=user.name, email=user.email, address1=user.locality, address2=user.locality, city=user.city, postcode=user.zipcode, country='Bangladesh', phone=user.mobile)

    mypayment.set_shipping_info(shipping_to=user.name, address=user.locality, city=user.city, postcode=user.zipcode, country='Bangladesh')

    response_data = mypayment.init_payment()
   
   
    return redirect(response_data['GatewayPageURL'])




@csrf_exempt
def complete(request):
    # handle successful payment response from SSLCommerz
    if request.method == 'POST' or request.method == 'post':
        payment_data=request.POST
        status=payment_data['status']
        
        
        if status == 'VALID':
            val_id=payment_data['val_id']
            tran_id=payment_data['tran_id']
            bank_tran_id=payment_data['bank_tran_id']
            card_type=payment_data['card_type']
            
            messages.success(request,f"your payment completed successfully")
            return HttpResponseRedirect(reverse('purchase', kwargs={'val_id': val_id, 'tran_id': tran_id}))


        elif status == 'FAILED':
            messages.warning(request,f"your payment Failed .please try again")
    return render(request, 'app/complete.html')
@login_required
def purchase(request, val_id, tran_id):
    cart = Cart.objects.filter(user=request.user, purchased=False)
    orders = []
    for c in cart:
        order = OrderPlaced(
            user=request.user,
            
            product=c.product,
            quantity=c.quantity,
          
            ordered=True,
            payment_Id=val_id,
            order_Id=tran_id,
            status='pending',
        )
        orders.append(order)
        order.save()
        c.purchased = True
        c.save()
        c.delete()
    return HttpResponseRedirect(reverse('home'))



def payment_success(request):
    # handle successful payment response from SSLCommerz
    return render(request, 'app/success.html',context=())

def payment_fail(request):
    # handle failed payment response from SSLCommerz
    return render(request, 'app/fail.html')

def payment_cancel(request):
    # handle canceled payment response from SSLCommerz
    return render(request, 'app/cancel.html')


def add_review(request, pk):
    products = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = products
            review.user = request.user
            review.save()
            return redirect('product-detail', pk=products.pk)
    else:
        form = ReviewForm()
    return render(request, 'app/add_review.html', {'products': products, 'form': form})

@login_required
def wishlist(request):
    totalitem = 0
    user = request.user
    wishlist_products = Wishlist.objects.filter(user=user).exclude(product__cart__user=user)
    
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    return render(request, 'app/wishlist.html', {'wishlist_products': wishlist_products, 'totalitem': totalitem})


@login_required
def add_to_wishlist(request, pk):
    totalitem=0
    user = request.user
 
    product = Product.objects.get(pk=pk)   # retrieve the Product instance
    
    # Check if the product is already in the user's wishlist
    if user.wishlist.filter(product=product).exists():
        messages.info(request, 'Product is already in your wishlist.')
    else:
        # Add the product to the user's wishlist
        Wishlist.objects.create(user=user, product=product).save()
        messages.success(request, '')
    print(f"User: {user.username}")
    print(f"Product added to wishlist: {product.title}")
    if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
    return redirect('/wishlist', {'totalitem':totalitem})


  