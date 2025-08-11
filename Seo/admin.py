from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import SEOPage, Keyword


@admin.register(SEOPage)
class SEOPageAdmin(TranslationAdmin):
    list_display = ('page_url', 'title', 'description')
    search_fields = ('page_url', 'title')


class KeywordAdmin(TranslationAdmin):
    list_display = ('name',)


admin.site.register(Keyword, KeywordAdmin)
