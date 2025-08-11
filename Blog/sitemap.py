from django.contrib.sitemaps import Sitemap
from django.utils.translation import activate

from .models import BlogPost
from django.urls import reverse


class BlogPostListSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        # فقط یک لینک به صفحه اصلی لیست مقالات برمی‌گرداند
        return ['blogs:blog-view']

    def location(self, item):
        return reverse(item)


class BlogPostDetailSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return BlogPost.objects.all()

    def location(self, obj):
        activate(obj.language)  # تغییر زبان
        # آدرس جزئیات مقاله را برمی‌گرداند
        return reverse('blogs:detail', kwargs={'slug': obj.slug})

    def lastmod(self, obj):
        # تاریخ آخرین به‌روزرسانی مقاله
        return obj.published_date



