# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.contrib.contenttypes.generic import GenericTabularInline, BaseGenericInlineFormSet

from models import ImageOfModel

class ImageFormset(BaseGenericInlineFormSet):
    
    def clean(self):
        if not self.files.values() and not self.instance.images.all():
            raise forms.ValidationError(u'Загрузите хотябы одну фотографию')

class ImageOfModelInline(GenericTabularInline):
    model = ImageOfModel
    formset = ImageFormset
    extra = 1

class OneImageOfModelInline(ImageOfModelInline)
    max_num = 1
