from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe

from content.models import Content


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )


    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    company = models.CharField(max_length=100)
    address = models.CharField(blank=True,max_length=150)
    phone = models.CharField(blank=True,max_length=30)
    fax = models.CharField(blank=True,max_length=30)
    email = models.CharField(blank=True,max_length=50)
    smtpserver = models.CharField(blank=True,max_length=150)
    smtpemail = models.CharField(blank=True,max_length=150)
    smtppassword = models.CharField(blank=True,max_length=150)
    smtpport = models.CharField(blank=True,max_length=5)
    icon = models.ImageField(blank=True,upload_to='images/')
    facebook = models.CharField(blank=True,max_length=150)
    twitter = models.CharField(blank=True,max_length=150)
    instagram = models.CharField(blank=True,max_length=150)
    aboutus = RichTextUploadingField(blank=True,)
    contact = RichTextUploadingField(blank=True,)
    references = RichTextUploadingField(blank=True,)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )


    name = models.CharField(blank=True, max_length=30)
    email = models.CharField(blank=True,max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.CharField(blank=True, max_length=255)
    status = RichTextUploadingField(default='New', max_length=10, choices=STATUS)
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactFormu(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name' : TextInput(attrs={'class':'span4 form-group','placeholder':'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'span4 form-group', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'span4 form-group', 'placeholder': 'Email'}),
            'message': Textarea(attrs={'class': 'span4 form-group', 'placeholder': 'Your Message', 'rows':'10'}),
        }


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=30)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=30)
    country = models.CharField(blank=True, max_length=30)
    image = models.ImageField(blank=True, upload_to='images/users')
    cv = RichTextUploadingField()

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' +self.user.last_name +' ''['+ self.user.username + ']'


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country','image']


class FAQ(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    ordernumber = models.IntegerField()
    question = models.CharField(max_length=150)
    answer = models.TextField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
        

