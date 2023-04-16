from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('CR', 'Curd'),
    ('ML', 'Milk'),
    ('LS', 'Lassi'),
    ('MS', 'Milkshake'),
    ('PN', 'Panner'),
    ('GH', 'Ghee'),
    ('CZ', 'Cheese'),
    ('IC', 'Ice-Creams'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product/%Y/%m/%d/')

    def __str__(self):
        return self.title

STATE_CHOISES = (
    ('Dolnośląskie', 'Dolnośląskie'),
    ('Kujawsko-pomorskie', 'Kujawsko-pomorskie'),
    ('Lubelskie', 'Lubelskie'),
    ('Lubuskie', 'Lubuskie'),
    ('Łódzkie', 'Łódzkie'),
    ('Małopolskie', 'Małopolskie'),
    ('Mazowieckie', 'Mazowieckie'),
    ('Opolskie', 'Opolskie'),
    ('Podkarpackie', 'Podkarpackie'),
    ('Podlaskie', 'Podlaskie'),
    ('Pomorskie', 'Pomorskie'),
    ('Śląskie', 'Śląskie'),
    ('Świętokrzyskie', 'Świętokrzyskie'),
    ('Warmińsko-mazurskie', 'Warmińsko-mazurskie'),
    ('Wielkopolskie', 'Wielkopolskie'),
    ('Zachodniopomorskie', 'Zachodniopomorskie'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOISES, max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    stripe_order_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_payment_status = models.CharField(max_length=100, blank=True, null=True)
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default='')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)