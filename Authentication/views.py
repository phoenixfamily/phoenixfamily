from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from User.models import User
from .models import OTPVerification
from .serializers import RegisterSerializer, LoginSerializer, RequestOTPSerializer, VerifyOTPSerializer, \
    OTPVerificationSerializer
import random
import hashlib
from django.utils.timezone import now, timedelta
from .utils import send_otp_email


class RegisterView(APIView):
    """Handles user registration."""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": f"User: {user.id} registered. Please verify email."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestOTPView(APIView):
    """Generate and send OTP."""

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            # Generate OTP
            otp_code = str(random.randint(100000, 999999))
            otp_hash = hashlib.sha256(otp_code.encode()).hexdigest()

            otp_record, created = OTPVerification.objects.get_or_create(user=user)
            otp_record.otp_hash = otp_hash
            otp_record.expires_at = now() + timedelta(minutes=5)
            otp_record.attempts = 0  # Reset attempts
            otp_record.save()

            # ✅ Send OTP via Email using the helper function
            send_otp_email(email, otp_code)

            return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPCRUDView(ModelViewSet):
    queryset = OTPVerification.objects.all()
    serializer_class = OTPVerificationSerializer

class VerifyOTPView(APIView):
    """Verify OTP and activate user."""
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            user.is_verified = True
            user.is_active = True
            user.assign_username()
            user.save(update_fields=["is_verified", "username", "is_active"])

            OTPVerification.objects.filter(user=user).delete()  # Remove OTP record

            return Response({"message": "OTP verified. Account activated."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Login API using JWT"""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
