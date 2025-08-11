from modeltranslation.translator import translator, TranslationOptions
from .models import *


class SEOPageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')  # فیلدهایی که باید ترجمه شوند


translator.register(SEOPage, SEOPageTranslationOptions)  # ثبت مدل برای ترجمه


class KeywordTranslationOptions(TranslationOptions):
    fields = ('name',)  # فقط نام کلمه کلیدی را ترجمه کن


translator.register(Keyword, KeywordTranslationOptions)
