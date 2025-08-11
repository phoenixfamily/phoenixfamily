from modeltranslation.translator import translator, TranslationOptions
from .models import *


class ContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')  # فیلدهایی که باید ترجمه شوند


translator.register(Content, ContentTranslationOptions)  # ثبت مدل برای ترجمه


class VisionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')  # فیلدهایی که باید ترجمه شوند


translator.register(Vision, VisionTranslationOptions)  # ثبت مدل برای ترجمه


class FeaturesTranslationOptions(TranslationOptions):
    fields = ('title', 'description')  # فیلدهایی که باید ترجمه شوند


translator.register(Features, FeaturesTranslationOptions)  # ثبت مدل برای ترجمه
