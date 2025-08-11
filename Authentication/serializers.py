from rest_framework import serializers
from User.models import User
from .models import OTPVerification
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """Ensure passwords match and number is unique."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        return data

    def create(self, validated_data):
        """Create a new user with `is_temporary=False`."""
        validated_data.pop('password2')  # Remove password2 since it's not in the model
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_temporary=False  # Ensure new users are not temporary
        )
        return user


class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = "__all__"

class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if email exists and user is not verified."""
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("No user found with this email.")
        if user.is_verified:
            raise serializers.ValidationError("User already verified.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        """Validate OTP."""
        email = data["email"]
        otp = data["otp"]
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User not found.")

        otp_record = OTPVerification.objects.filter(user=user).first()

        if not otp_record:
            raise serializers.ValidationError("No OTP found for this user.")

        valid, message = otp_record.is_valid(otp)
        if not valid:
            raise serializers.ValidationError(message)

        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate user with email & password."""
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user_id": user.id,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
