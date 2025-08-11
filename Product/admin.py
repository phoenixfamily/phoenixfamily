from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Product, Features


class ProductAdmin(TranslationAdmin):
    list_display = ('title', 'description', 'name', 'header', 'content')


admin.site.register(Product, ProductAdmin)


class FeaturesAdmin(TranslationAdmin):
    list_display = ('title', 'description')


admin.site.register(Features, FeaturesAdmin)
