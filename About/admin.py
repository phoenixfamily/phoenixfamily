from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import FAQ, AboutUs


class FAQAdmin(TranslationAdmin):
    list_display = ('title', 'description')


admin.site.register(FAQ, FAQAdmin)


class AboutUsAdmin(TranslationAdmin):
    list_display = ('title', 'description', 'name', 'alt', 'context')


admin.site.register(AboutUs, AboutUsAdmin)
