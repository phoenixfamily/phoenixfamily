from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import test_path

router = DefaultRouter()
router.register(r'seo', views.SEOPageView, basename='seo')
router.register(r'keyword', views.KeywordView, basename='keyword')

app_name = 'seo'

urlpatterns = [
    path('api/', include(router.urls)),
    path('test-path/', test_path, name='test_path'),

]
