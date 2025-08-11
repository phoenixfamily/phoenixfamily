from modeltranslation.translator import translator, TranslationOptions
from .models import *


class AboutUsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'name', 'alt', 'context')  # فیلدهایی که باید ترجمه شوند


translator.register(AboutUs, AboutUsTranslationOptions)  # ثبت مدل برای ترجمه


class FAQTranslationOptions(TranslationOptions):
    fields = ('title', 'description')  # فیلدهایی که باید ترجمه شوند


translator.register(FAQ, FAQTranslationOptions)  # ثبت مدل برای ترجمه

