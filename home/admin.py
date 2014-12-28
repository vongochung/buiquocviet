# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from home.models import  POST,Category, IMAGE_STORE


class POSTForm(forms.ModelForm):

    class Meta:
        model = POST
        fields = ('title','title_en', 'link','content', 'description','description_en' , 'category')


class CustomPOSTAdmin(admin.ModelAdmin):
    fieldsets = None
    list_display = ('title', 'comments')
    form = POSTForm
    def save_model(self, request, obj, form, change): 
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return instance

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name','name_en', 'parent_id', 'order')


class CustomCategoryAdmin(admin.ModelAdmin):
    fieldsets = None
    list_display = ('name', 'order')
    form = CategoryForm

class CustomIMAGEAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)
    list_display = ('file_name', 'image_tag',)

admin.site.register(IMAGE_STORE, CustomIMAGEAdmin)
admin.site.register(POST, CustomPOSTAdmin)
admin.site.register(Category, CustomCategoryAdmin)