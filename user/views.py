from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import UserProfile
from product.models import Category


def index(request):
    category = Category.objects.all()
    current_user = request.user  # Access user session information
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {
        'category': category,
        'profile' : profile,
    }
    return render(request,'user_profile.html',context)