from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.userDB import User, OTP
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers.authenticationSZ import TelegramOTPStoreSerializer,OTPVerifyCodeOnlySerializer
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample



@extend_schema(
    tags=["Authentication"],
    summary="Store Telegram OTP",
    description="Accepts Telegram OTP and links it to a phone number + telegram_id. Creates user if they don't exist.",
    request=TelegramOTPStoreSerializer,
    responses={
        200: OpenApiResponse(description="OTP saved"),
        400: OpenApiResponse(description="Invalid input"),
    }
)
class TelegramOTPStoreAPIView(APIView):
    permission_classes = []
    serializer_class = TelegramOTPStoreSerializer

    def post(self, request):
        serializer = TelegramOTPStoreSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        phone = data["phone_number"]
        telegram_id = data["telegram_id"]
        code = data["code"]

        user, _ = User.objects.get_or_create(phone_number=phone, defaults={"username": phone})
        user.telegram_id = telegram_id
        user.save()

        OTP.objects.create(user=user, code=code)
        return Response({"status": "OTP saved"})

    

@extend_schema(
    tags=["Authentication"],
    summary="Verify OTP and get JWT token",
    description="Checks if an OTP code is valid and unused. If valid, returns JWT access and refresh tokens.",
    request=OTPVerifyCodeOnlySerializer,
    responses={
        200: OpenApiResponse(
            description="JWT tokens issued",
            examples=[
                {
                    "access": "eyJ0eXAiOiJKV1QiLCJh...",
                    "refresh": "eyJ0eXAiOiJKV1QiLCJh..."
                }
            ]
        ),
        400: OpenApiResponse(description="Invalid or expired code"),
    }
)
class OTPVerifyJWTAPIView(APIView):
    permission_classes = []
    serializer_class = OTPVerifyCodeOnlySerializer
   
    def post(self, request):
        serializer = OTPVerifyCodeOnlySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        code = serializer.validated_data['code']
        otp = OTP.objects.filter(code=code, used=False).order_by('-created_at').first()

        if not otp or not otp.is_valid():
            return Response({"error": "Invalid or expired code"}, status=400)

        otp.used = True
        otp.save()

        user = otp.user
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Refresh JWT token",
        description="Provide a refresh token to get a new access token.",
        responses={
            200: OpenApiResponse(
                description="New access token",
                examples=[{
                    "access": "new_access_token_here"
                }]
            ),
            401: OpenApiResponse(description="Invalid refresh token")
        }
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    pass