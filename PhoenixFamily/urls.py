from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import RedirectView

from Blog.sitemap import *
from PhoenixFamily import settings
from django.conf.urls.i18n import set_language

from PhoenixFamily.views import robots_txt
from Product.sitemaps import ProductSitemap
from Seo.sitemaps import StaticViewSitemap

sitemaps = {
    'blog_list': BlogPostListSitemap,
    'blog_details': BlogPostDetailSitemap,
    'static': StaticViewSitemap(),
    'product': ProductSitemap(),

}

urlpatterns = [
    path('admin/', admin.site.urls),  # مسیر پنل ادمین
    path('set_language/', set_language, name='set_language'),  # به جای include از set_language استفاده کنید
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path("robots.txt", robots_txt, name="robots_txt"),

]

urlpatterns += i18n_patterns(
    path('about/', include('About.urls', namespace='about')),  # مسیر URLهای اپلیکیشن About
    path('blogs/', include('Blog.urls', namespace='blogs')),  # مسیر URLهای اپلیکیشن Blog
    path('contact/', include('Contact.urls', namespace='contact')),  # مسیر URLهای اپلیکیشن Contact
    path('home/', include('Home.urls', namespace='home')),  # مسیر URLهای اپلیکیشن Home
    path('products/', include('Product.urls', namespace='products')),  # مسیر URLهای اپلیکیشن Product
    path('user/', include('User.urls', namespace='user')),  # مسیر URLهای اپلیکیشن User
    path('auth/', include('Authentication.urls', namespace='authentication')),  # مسیر URLهای اپلیکیشن Authentication
    path('seo/', include('Seo.urls', namespace='seo')),  # مسیر URLهای اپلیکیشن Authentication
    path('webmail/', include('WebMail.urls', namespace='webmail')),  # مسیر URLهای اپلیکیشن Authentication
    path('', RedirectView.as_view(url='home/', permanent=True)),  # ریدایرکت دائمی

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
