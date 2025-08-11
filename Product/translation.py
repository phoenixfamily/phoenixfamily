from modeltranslation.translator import translator, TranslationOptions
from .models import *


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'name', 'header', 'content')  # فیلدهایی که باید ترجمه شوند


translator.register(Product, ProductTranslationOptions)  # ثبت مدل برای ترجمه


class FeaturesTranslationOptions(TranslationOptions):
    fields = ('title', 'description')  # فیلدهایی که باید ترجمه شوند


translator.register(Features, FeaturesTranslationOptions)  # ثبت مدل برای ترجمه
