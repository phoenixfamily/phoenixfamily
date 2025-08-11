from django.urls import path, include
from .views import products, ProductView, FeaturesView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product', ProductView, basename='product')
router.register(r'features', FeaturesView, basename='features')


app_name = 'products'

urlpatterns = [
    path('<int:pk>/', products, name='product-view'),  # صفحه اصلی
    path('api/', include(router.urls)),
]
