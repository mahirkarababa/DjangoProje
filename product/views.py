from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.models import CommentForm, Comment


def index(request):
    return HttpResponse("Product Page")

@login_required(login_url='/login') #Check Login
def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user  # Access user session information

            data = Comment() #model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')  # İP AL
            data.save()

            messages.success(request, "Yorumunuz Başarılı Şekilde Gönderilmiştir.")

            return HttpResponseRedirect(url)
        messages.error(request, "Yorumunuz Kaydedilmedi. Tekrar yapın")
        return HttpResponseRedirect(url)



