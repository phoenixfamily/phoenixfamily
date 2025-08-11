from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product  # مدل محصولت رو ایمپورت کن


class ProductSitemap(Sitemap):
    changefreq = "daily"  # بسته به به‌روزرسانی سایت، می‌تونی تنظیمش کنی
    priority = 0.9 # اهمیت صفحه برای گوگل
    protocol = 'https'  # اگر سایتت SSL داره

    def items(self):
        return Product.objects.all()  # فقط محصولات فعال رو بگیر

    def location(self, item):
        return reverse('products:product-view', args=[item.id])  # اگه از ID استفاده می‌کنی

        # اگر از Slug استفاده می‌کنی، این رو جایگزین کن:
        # return reverse('product_detail', args=[item.slug])
