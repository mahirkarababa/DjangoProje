from django.contrib import admin

# Register your models here.
from order.models import ShopCart, OrderProduct, Order


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','product','salary','quantity']
    list_filter = ['user']




class OrderProdcutline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user','product','salary','quantity','amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone','city','total','status']
    list_filter = ['status']
    readonly_fields = ('user','address','city','country','phone','first_name','last_name','ip','total')
    can_delete = False
    inlines = [OrderProdcutline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'salary', 'quantity', 'amount']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
