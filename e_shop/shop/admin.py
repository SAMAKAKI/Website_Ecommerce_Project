from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Group

from .models import *


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products', 'quantity']

    def products(self, obj):
        link = reverse("admin:shop_product_change", args=[obj.product.pk])
        return format_html(f'<a href="{link}">{obj.product.title}</a>')


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'stripe_order_id', 'stripe_payment_status', 'stripe_payment_id', 'paid']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customers', 'products', 'quantity', 'ordered_date', 'status', 'payments']

    def products(self, obj):
        link = reverse("admin:shop_product_change", args=[obj.product.pk])
        return format_html(f'<a href="{link}">{obj.product.title}</a>')

    def customers(self, obj):
        link = reverse("admin:shop_customer_change", args=[obj.customer.pk])
        return format_html(f'<a href="{link}">{obj.customer.name}</a>')

    def payments(self, obj):
        link = reverse("admin:shop_payment_change", args=[obj.payment.pk])
        return format_html(f'<a href="{link}">{obj.payment.stripe_payment_id}</a>')

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products']

    def products(self, obj):
        link = reverse("admin:shop_product_change", args=[obj.product.pk])
        return format_html(f'<a href="{link}">{obj.product.title}</a>')

admin.site.unregister(Group)