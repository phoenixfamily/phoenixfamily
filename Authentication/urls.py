from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, RequestOTPView, OTPCRUDView, VerifyOTPView

app_name = "user"

router = DefaultRouter()
router.register(r"otp-crud", OTPCRUDView, basename='otp-crud')

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/request-otp/', RequestOTPView.as_view(), name='request_otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    # Include the router URLs for UserCRUDView
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
]
