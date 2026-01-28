from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_email
from accounts.models import EmailVerification
from .utiles import send_verification_code
from .serializers import ( 
    ResendVerificationCodeSerializer, 
    SignUpSerializer, 
    CustomTokenObtainPairSerializer, 
    EmailVerificationSerializer, 
    ChangePasswordSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer
)
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .throttles import EmailVerificationThrottle
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([EmailVerificationThrottle])
def sign_up(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Verification code sent to your email."}, status=status.HTTP_201_CREATED)
    

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def custom_token_obtain_pair_view(request):
    if request.method == 'POST':
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@permission_classes([AllowAny])
def email_verification(request):
    serializer = EmailVerificationSerializer(data=request.data)
    if serializer.is_valid():
        code = serializer._validated_data['code']

        try:
            verification_record = EmailVerification.objects.get(code=code)
        except EmailVerification.DoesNotExist:
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

        if verification_record.is_expired():
            return Response({"error": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user = verification_record.user
        user.is_email_verified = True
        user.is_active = True
        user.save()

        verification_record.delete()

        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([EmailVerificationThrottle])
def resend_verification_code(request):
    serializer = ResendVerificationCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer._validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_email_verified:
            return Response({"message": "Email is already verified."}, status=status.HTTP_200_OK)

        send_verification_code(user.id)

        return Response({"message": "New verification code sent to your email."}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data = request.data)

    if serializer.is_valid(raise_exception=True):
        new_password = serializer.validated_data['new_password']
        old_password = serializer.validated_data['old_password']
        user = request.user

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([EmailVerificationThrottle])
def forget_password_view(request):
    serializer = ForgetPasswordSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer._validated_data['email']

        try:
            user = User.objects.get(email = email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = user.id
            message = f"http://127.0.0.1:8000/forget-passwrod/{uid}/{token}"
            subject = 'Forget Password'
            send_email.delay(uid, subject, message)
            return Response({"message": "Check your email"})
        except User.DoesNotExist:
            return Response({"message": "Your email doesn't exist"})


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_view(request):
    serializer = ResetPasswordSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)