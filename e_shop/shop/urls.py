from django.urls import path
from .views import *
from .forms import *
from django.contrib.auth import views as auth_view
from django.contrib import admin

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('category/<slug:cat_value>', CategoryView.as_view(), name='category'),
    path('category-title/<value>', CategoryTitleView.as_view(), name='category_title'),
    path('product-detail/<int:prod_value>', ProductDetail.as_view(), name='product_detail'),
    path('profile/', CustomerProfileView.as_view(), name='profile'),
    path('address/', address, name='address'),
    path('update-address/<int:pk>', UpdateAddressView.as_view(), name='update_address'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', show_cart, name='show_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('plus-cart/', plus_cart, name='plus_cart'),
    path('minus-cart/', minus_cart, name='minus_cart'),
    path('remove-cart/', remove_cart, name='remove_cart'),
    path('plus-wishlist/', plus_wishlist, name='plus_wishlist'),
    path('minus-wishlist/', minus_wishlist, name='minus_wishlist'),
    path('wishlist/', WishlistView.as_view(), name='show_wishlist'),
    path('search/', search, name='search'),

    # login authentication
    path('register/', CustomerRegistrationView.as_view(), name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='shop/login.html', authentication_form=CustomerLoginFrom), name='login'),
    path('password-change/', auth_view.PasswordChangeView.as_view(template_name='shop/password_change.html', form_class=MyPasswordChangeForm, success_url='/password-change-done'), name='password_change'),
    path('password-change-done/', auth_view.PasswordChangeDoneView.as_view(template_name='shop/password_change_done.html'), name='password_change_done'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='shop/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='shop/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='shop/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='shop/password_reset_complete.html'), name='password_reset_complete'),
]

admin.site.site_header = 'SAMAKAKI Dairy'
admin.site.site_title = 'SAMAKAKI Dairy'
admin.site.site_index_title = 'Welcome to SAMAKAKI Dairy Shop'