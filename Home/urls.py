from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'content', views.ContentView, basename='content')
router.register(r'vision', views.VisionView, basename='vision')
router.register(r'features', views.FeaturesView, basename='features')


app_name = 'home'

urlpatterns = [
    path('', views.home, name='home-view'),  # صفحه اصلی
    path('api/', include(router.urls)),
]
