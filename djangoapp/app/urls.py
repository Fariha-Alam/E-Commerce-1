from django.urls import path, re_path

from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,passwordChange,passwordReset,Mysetpassword
from app.views import ProfileEditView,SearchView,wishlist
from .views import add_review

urlpatterns = [
   # path('', views.home),
    path('', views.ProductView.as_view(), name='home'),
    path('', views.MainProductView.as_view(), name='home'),
    path('products/', views.ProductView.as_view(), name='product_view'),

   

    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('main-product-detail/<int:pk>', views.ProductDetailView.as_view(), name='main-product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),

    path('profile/', views.profileView.as_view(), name='profile'),
    path('edit-profile/', ProfileEditView.as_view(), name='profile-edit'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('laptop/', views.laptop, name='laptop'),
    path('cloth/', views.cloth, name='cloth'),
    path('grocery/', views.grocery, name='grocery'),
    path('camera/', views.camera, name='camera'),

    path('mobile/<str:data>', views.mobile, name='mobiledata'),

    path('laptop/<str:data>', views.laptop, name='laptopdata'),
    path('cloth/<str:data>', views.cloth, name='clothdata'),
    path('grocery/<str:data>', views.grocery, name='grocerydata'),
    path('camera/<str:data>', views.camera, name='cameradata'),

    path('search/', SearchView.as_view(), name='search'),

    path('products/<int:pk>/review/', views.add_review, name='add_review'),

    path('wishlist/', wishlist, name='wishlist'),
    path('wishlist/add/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordChange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordChange.html',form_class=passwordChange,success_url='/passwordChangeDone/'), name='passwordchange'),
    path('passwordChangeDone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordChangeDone.html'), name='passwordChangeDone'),    
    path('passwordReset/', auth_views.PasswordResetView.as_view(template_name='app/passwordReset.html',form_class=passwordReset,success_url='/password_reset/done/'), name='passwordReset'),



    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/passwordReset_Done.html'), name='passwordReset_Done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html',
        form_class=Mysetpassword
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/<val_id>/<tran_id>/', views.payment_done, name='paymentdone'),
    path('purchase/<val_id>/<tran_id>/', views.purchase, name='purchase'),
    

    path('payment/', views.payment, name='payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('complete/', views.complete, name='complete'),
    path('fail/', views.payment_fail, name='payment_fail'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
