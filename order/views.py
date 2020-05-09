from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import UserProfile
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct
from product.models import Category, Product


def index(request):
    return HttpResponse("Order App")


@login_required(login_url='/login') #CHECK LOGİN
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER') #GET LAST URL
    current_user = request.user
    #****ÜRÜN SEPETTE VAR MI?
    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1  # Ürün Var
    else:
        control = 0
    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
                messages.warning(request, "Başvuruda Hata Oluştu")
                return HttpResponseRedirect(url)
                # return HttpResponse("Kaydedildi")
                #data = ShopCart.objects.get(product_id=id)
                #data.quantity += form.cleaned_data['quantity']
                #data.save()  #veritabanına kaydet
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
                request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  #COUNT THE İTEM İN SHOP CART
                messages.success(request, "İlan Başarı ile Başvurularınıza Eklenmiştir.")
                return HttpResponseRedirect(url)
                #return HttpResponse("Kaydedildi")

    messages.warning(request, "Başvuruda Hata Oluştu")
    return HttpResponseRedirect(url)
    #return HttpResponse("Kaydedildi")



@login_required(login_url='/login') #CHECK LOGİN
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # COUNT THE İTEM İN SHOP CART

    total = 0

    for rs in shopcart:
        total += rs.product.salary * rs.quantity

    context = {
        'shopcart' : shopcart,
        'category' : category,
        'total' : total,
    }
    return render(request,'shopcart_products.html',context)



@login_required(login_url='/login') #CHECK LOGİN
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # COUNT THE İTEM İN SHOP CART
    messages.success(request,"İlan Başvurularınızdan Silindi")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login') #CHECK LOGİN
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.salary * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper
            data.code = ordercode
            data.save()

            #MOVE SHOPCART İTEMS TO ORDER PRODUCTS İTEMS
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id       # order id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.salary = rs.product.salary
                detail.amount = rs.amount
                detail.save()

                #REDUCE QUANTİTY OF SOLD PRODUCT FROM AMOUNT OF PRODUCT
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()



            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            #return HttpResponse("Tamamlandı")
            messages.success(request, "Başvurunuz Tamamlandı")
            return render(request, 'Order_Complated.html',{'ordercode':ordercode,'category':category})
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user)
    context = {
        'shopcart' : shopcart,
        'category': category,
        'total': total,
        'form': form,
        'profile': profile,
    }
    return  render(request,'Order_Form.html',context)

