from django.urls import path
from . import views
from .views import EmailView

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact-view'),  # صفحه اصلی
    path('api/', EmailView.as_view(), name='email'),

]
