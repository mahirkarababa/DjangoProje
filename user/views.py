from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render, redirect

# Create your views here.
from content.models import Menu, ContentForm, Content, ContentImageForm, CImages
from home.models import UserProfile
from order.models import Order, OrderProduct
from product.models import Category, Comment
from user.forms import UserUpdateForm, ProfileUpdateForm

@login_required(login_url='/login') #CHECK LOGİN
def index(request):
    category = Category.objects.all()
    current_user = request.user  # Access user session information
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {
        'category': category,
        'profile' : profile,
    }
    return render(request,'user_profile.html',context)

@login_required(login_url='/login') #CHECK LOGİN
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user) #REQUES.USER İS USER SESSİON DATA
        # "İNSTANCE=REQUEST.USER.USERPROFİLE" COMES FROM "USERPROFILE" MODEL -> OneTwoOne RELATION
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your Account has been updated!')
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category' : category,
            'user_form' : user_form,
            'profile_form' : profile_form,
        }
        return render(request,'user_update.html',context)

@login_required(login_url='/login') #CHECK LOGİN
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Your Password Was Successfully Updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request,'Please Correct The Error Below. <br>' +str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',{
            'form' : form, 'category' : category
        })

@login_required(login_url='/login') #CHECK LOGİN
def orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'orders': orders,
    }
    return render(request, 'user_orders.html',context)

@login_required(login_url='/login') #CHECK LOGİN
def orderdetail(request,id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id,id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login') #CHECK LOGİN
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login') #CHECK LOGİN
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id,user_id=current_user.id).delete()
    messages.success(request, 'Comment Deleted')
    return HttpResponseRedirect("/user/comments")

@login_required(login_url='/login') #CHECK LOGİN
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST,request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request,'Your Content Inserted Seccessfuly')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category = Category.objects.all()
        form = ContentForm()
        menu = Menu.objects.all()
        context = {
            'category': category,
            'form': form,
            'menu': menu,
        }
        return render(request, 'user_addcontent.html', context)

@login_required(login_url='/login') #CHECK LOGİN
def contentedit(request,id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request,'Your Content Inserted Seccessfuly')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit' + str(id))
    else:
        category = Category.objects.all()
        form = ContentForm(instance=content)
        menu = Menu.objects.all()
        context = {
            'category': category,
            'form': form,
            'menu': menu,
        }
        return render(request, 'user_addcontent.html', context)





@login_required(login_url='/login') #CHECK LOGİN
def contents(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'menu': menu,
        'contents': contents,
    }
    return render(request, 'user_contents.html', context)

@login_required(login_url='/login') #CHECK LOGİN
def contentdelete(request,id):
    current_user=request.user
    Content.objects.filter(id=id,user_id=current_user.id).delete()
    messages.success(request,'Content deleted..')
    return HttpResponseRedirect('/user/contents')


def contentaddimage(request,id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = ContentImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = CImages()
            data.title = form.cleaned_data['title']
            data.content_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request,'Your Image has been Seccessfuly upload')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error :' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        content = Content.objects.get(id=id)
        images = CImages.objects.filter(content_id=id)
        form = ContentImageForm(instance=content)
        context = {
            'content': content,
            'images': images,
            'form': form,
        }
        return render(request, 'content_gallery.html', context)