from modeltranslation.translator import translator, TranslationOptions
from .models import *


class BlogPostTranslationOptions(TranslationOptions):
    fields = (
        'title', 'content', 'slug', 'meta_title', 'meta_description')  # فیلدهایی که باید ترجمه شوند


translator.register(BlogPost, BlogPostTranslationOptions)  # ثبت مدل برای ترجمه
