from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from ..models import User
from utils import OtpManager, RedisManager
from datetime import date, datetime
from ..serializers.user_serializers import UserRegisterSerializer, VerifyOtpCodeSerializer, LoginByEmailSerializer, LoginByPhoneNumber, UserProfileSerializer
from cms.models import Disease
from django.core import serializers as ser
import json
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            for key, value in serializer.validated_data.items():
                if isinstance(value, (date, datetime)):
                    serializer.validated_data[key] = value.isoformat()


            disease_queryset = serializer.validated_data.get('disease', [])
            serialized_disease = ser.serialize('json', disease_queryset)
            deserialized_disease = json.loads(serialized_disease)
            disease_names = [item['fields']['name'] for item in deserialized_disease]
            print('*' * 80, disease_names)
            request.session['user_info'] = {
                'phone_number': serializer.validated_data['phone_number'],
                'fullname': serializer.validated_data['fullname'],
                'email': serializer.validated_data['email'],
                'password': serializer.validated_data['password'],
                'job_pollution_level': serializer.validated_data['job_pollution_level'],
                'job_category': serializer.validated_data['job_category'],
                'seasonal_allergy': serializer.validated_data['seasonal_allergy'],
                'taste_sensitivity': serializer.validated_data['taste_sensitivity'],
                'date_of_birth' : serializer.validated_data['date_of_birth'],
                'gender': serializer.validated_data['gender'],
                'disease': disease_names
            }

            otp_code = OtpManager.generate_otp_code()
            print('----' * 80, otp_code)
            OtpManager.send_otp_code(serializer.validated_data['phone_number'], otp_code)
            RedisManager().add_to_redis(serializer.validated_data['phone_number'], otp_code)
            return Response({'message': 'اطلاعات شما وارد شد'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOtpCodeView(CreateAPIView):
    serializer_class = VerifyOtpCodeSerializer
    permission_classes = (AllowAny, )
    
    def create(self, request, *args, **kwargs):
        user_session = request.session['user_info']
        if not user_session:
            return Response({'error': 'اطلاعات شما ثبت نشده است'}, status=status.HTTP_400_BAD_REQUEST)
        print(user_session)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            otp_code_entered = serializer.validated_data['code']
            phone_number = user_session['phone_number']
            
            redis_manager = RedisManager()
            sotred_otp_code = redis_manager.get_by_redis(phone_number=user_session['phone_number'])
            if str(otp_code_entered) == str(sotred_otp_code):
                user = User.objects.create_user(
                phone_number = user_session['phone_number'],
                email = user_session['email'],
                fullname = user_session['fullname'],
                job_pollution_level = user_session['job_pollution_level'],
                job_category = user_session['job_category'],
                seasonal_allergy = user_session['seasonal_allergy'],
                taste_sensitivity = user_session['taste_sensitivity'],
                date_of_birth = user_session['date_of_birth'],
                gender = user_session['gender'],
                password = user_session['password']
                )

                disease_names = user_session['disease']
                diseases = Disease.objects.filter(name__in=disease_names)
                user.disease.set(diseases)
                user.save()
                return Response({'manage': 'شما با موفقیت وارد شدید '}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'کد نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ObtainTokenByEmail(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        ser_data = LoginByEmailSerializer(data=request.data)
        if ser_data.is_valid():
            email = ser_data.validated_data['email']
            password = ser_data.validated_data['password']
            user = User.objects.filter(email=email).first()
            if user is not None and user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status= status.HTTP_200_OK)
            else:
                return Response({'error': 'ایمیل یا نام کاربری اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
        
class ObtainTokenByPhoneNumber(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        ser_data = LoginByPhoneNumber(data=request.data)
        if ser_data.is_valid():
            phone_number = ser_data.validated_data['phone_number']
            request.session['user_number'] = phone_number
            otp_code = OtpManager.generate_otp_code()
            print('----' * 80, otp_code)
            OtpManager.send_otp_code(ser_data.validated_data['phone_number'], otp_code)
            RedisManager().add_to_redis(ser_data.validated_data['phone_number'], otp_code)
            return Response({'message': "کد ارسال شد "}, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginVerifyOtpCode(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        user_number = request.session['user_number']
        ser_data = VerifyOtpCodeSerializer(data=request.data)
        if ser_data.is_valid():
            entered_otp_code = ser_data.validated_data['code']
            redis_manager = RedisManager()
            sotred_otp_code = redis_manager.get_by_redis(phone_number= user_number)
            if str(entered_otp_code) == str(sotred_otp_code):
                try:
                    user = User.objects.get(phone_number=user_number)
                except User.DoesNotExist:
                    return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token':token.key}, status=status.HTTP_202_ACCEPTED)
            return Response({'message': 'کد نامعتبر است '}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'با موفقیت خارج شدید'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )
    
    def get_object(self):
        return self.request.user
    
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        # Make a mutable copy of request data
        data = request.data.copy()
        # Remove non-updatable fields
        data.pop('phone_number', None)
        data.pop('email', None)
        # Update request data
        serializer = self.get_serializer(self.get_object(), data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        # Make a mutable copy of request data
        data = request.data.copy()
        # Remove non-updatable fields
        data.pop('phone_number', None)
        data.pop('email', None)
        # Update request data
        serializer = self.get_serializer(self.get_object(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)