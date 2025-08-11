from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutUsView, FAQView, about


app_name = 'about'

router = DefaultRouter()
router.register(r'about-us', AboutUsView, basename='about-us')
router.register(r'FAQ', FAQView, basename='faq')


urlpatterns = [
    path('', about, name='about-view'),  # صفحه اصلی
    path('api/', include(router.urls)),
]
