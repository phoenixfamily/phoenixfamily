from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *


class BlogPostAdmin(TranslationAdmin):
    list_display = ('title', 'content', 'slug', 'meta_title', 'meta_description')


admin.site.register(BlogPost, BlogPostAdmin)
