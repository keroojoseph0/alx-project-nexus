from rest_framework import serializers
from .utiles import send_verification_code
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length = 6)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        send_verification_code(user.id)

        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        is_email_verified = User.objects.filter(email=attrs['email'], is_email_verified=True).exists()
        if not is_email_verified:
            raise serializers.ValidationError('Email is not verified.')
        return super().validate(attrs)
    


class EmailVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)


class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only = True ,min_length=6)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        new_password = attrs.get("new_Password")
        uid = attrs.get('uid')
        token = attrs.get('token')

        try:
            user = User.objects.get(id = uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError("Invalid uid")

        token_generator = PasswordResetTokenGenerator()
        is_valid = token_generator.check_token(user, token)

        if not is_valid:
            raise serializers.ValidationError('Invalid or expired token')
        
        attrs['user'] = user
        return attrs
        
    def save(self):
        new_password = self.validated_data['new_password']
        user = self.validated_data['user']
        user.set_password(new_password)
        user.save()
        return user