from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages

def total_items_in_cart(request):
    totatlitem = 0
    if request.user.is_authenticated:
        totatlitem = len(Cart.objects.filter(user=request.user))
    return totatlitem

def total_items_in_wishlist(request):
    totalwishitem = 0
    if request.user.is_authenticated:
        totalwishitem = len(Wishlist.objects.filter(user=request.user))
    return totalwishitem

@login_required
def home(request):
    totalitem = total_items_in_cart(request)
    totalwishitem = total_items_in_wishlist(request)
    return render(request, 'shop/index.html', locals())

@login_required
def about(request):
    totalitem = total_items_in_cart(request)
    totalwishitem = total_items_in_wishlist(request)
    return render(request, 'shop/about.html', locals())

@login_required
def contact(request):
    totalitem = total_items_in_cart(request)
    totalwishitem = total_items_in_wishlist(request)
    return render(request, 'shop/contact.html', locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, cat_value):
        product = Product.objects.filter(category=cat_value)
        title = Product.objects.filter(category=cat_value).values('title')
        totalitem = total_items_in_cart(request)
        totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/category.html', locals())

@method_decorator(login_required, name='dispatch')
class CategoryTitleView(View):
    def get(self, request, value):
        product = Product.objects.filter(title=value)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = total_items_in_cart(request)
        totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/category.html', locals())

@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, prod_value):
        product = Product.objects.get(pk=prod_value)
        totalitem = total_items_in_cart(request)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/product_detail.html', locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = total_items_in_cart(request)
        totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! User Register Successfully!')
        else:
            messages.warning(request, 'Invalid Input Data')
            totalitem = total_items_in_cart(request)
            totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/customerregistration.html', locals())

@method_decorator(login_required, name='dispatch')
class CustomerProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = total_items_in_cart(request)
        totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations! User Profile Save Successfully!')
        else:
            messages.warning(request, 'Invalid Input Data')
            totalitem = total_items_in_cart(request)
            totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/profile.html', locals())

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = total_items_in_cart(request)
    totalwishitem = total_items_in_wishlist(request)
    return render(request, 'shop/address.html', locals())

@method_decorator(login_required, name='dispatch')
class UpdateAddressView(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = total_items_in_cart(request)
        totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/update_address.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']

            add.save()
            messages.success(request, 'Congratulations! User Profile Save Successfully!')
        else:
            messages.warning(request, 'Invalid Input Data')
        return redirect('address')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('show_cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for item in cart:
        value = item.quantity * item.product.discounted_price
        amount += value
    totalamount = amount + 40
    totalitem = total_items_in_cart(request)
    totalwishitem = total_items_in_wishlist(request)
    return render(request, 'shop/show_cart.html', locals())

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for item in cart_items:
            value = item.quantity * item.product.discounted_price
            famount += value
        totalamount = famount + 40
        totalitem = total_items_in_cart(request)
        totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/checkout.html', locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity += 1
        cart.save()
        user = request.user
        cart_filter = Cart.objects.filter(user=user)
        amount = 0
        for item in cart_filter:
            value = item.quantity * item.product.discounted_price
            amount += value
        totalamount = amount + 40
        # print(prod_id)
        data = {
            'quantity': cart.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity -= 1
        cart.save()
        user = request.user
        cart_filter = Cart.objects.filter(user=user)
        amount = 0
        for item in cart_filter:
            value = item.quantity * item.product.discounted_price
            amount += value
        totalamount = amount + 40
        # print(prod_id)
        data = {
            'quantity': cart.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.delete()
        user = request.user
        cart_filter = Cart.objects.filter(user=user)
        amount = 0
        for item in cart_filter:
            value = item.quantity * item.product.discounted_price
            amount += value
        totalamount = amount + 40
        # print(prod_id)
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@method_decorator(login_required, name='dispatch')
class WishlistView(View):
    def get(self, request):
        user = request.user
        wishlist = Wishlist.objects.filter(user=user)
        totalitem = total_items_in_cart(request)
        totalwishitem = total_items_in_wishlist(request)
        return render(request, 'shop/show_wishlist.html', locals())

@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(pk=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Wishlist Deleted Successfully',
        }
        return JsonResponse(data)

@login_required
def search(request):
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains=query))
    totalitem = total_items_in_cart(request)
    totalwishitem = total_items_in_wishlist(request)
    return render(request, 'shop/search.html', locals())