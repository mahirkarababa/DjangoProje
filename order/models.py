from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from product.models import Product


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product

    @property
    def amount(self):
        return (self.quantity * self.product.salary)

    @property
    def salary(self):
        return (self.product.salary)

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class Order(models.Model):
    STATUS = (
        ('Yeni', 'Yeni'),
        ('Başvuru Kabul Edildi', 'Başvuru Kabul Edildi'),
        ('Değenlediriliyor', 'Değenlediriliyor'),
        ('CV Değenlediriliyor', 'CV Değenlediriliyor'),
        ('Mülakat', 'Mülakat'),
        ('Reddedildi', 'Reddedildi'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    code = models.CharField(max_length=5,editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(blank=True,max_length=20)
    address = models.CharField(blank=True, max_length=130)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    total = models.FloatField()
    status = models.CharField(max_length=25,choices=STATUS,default='Yeni')
    ip = models.CharField(blank=True,max_length=20)
    adminnote = models.CharField(blank=True,max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','address','phone','city','country']



class OrderProduct(models.Model):
    STATUS = (
        ('Yeni', 'Yeni'),
        ('Kabul Edildi', 'Kabul Edildi'),
        ('Reddedildi', 'Reddedildi'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    salary = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=25,choices=STATUS,default='Yeni')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title