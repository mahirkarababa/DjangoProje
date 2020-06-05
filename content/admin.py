from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from content.models import Menu, Content, CImages


class ContentImageInline(admin.TabularInline):
    model = CImages
    extra = 3

class ContenAdmin(admin.ModelAdmin):
    list_display = ['title','type','image_tag','status','create_at']
    list_filter = ['status','type']
    inlines = [ContentImageInline]
    prepopulated_fields = {'slug':('title',)}


class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ['tree_actions', 'indented_title','status']
    list_filter = ['status']

admin.site.register(Menu, MenuAdmin)
admin.site.register(Content, ContenAdmin)