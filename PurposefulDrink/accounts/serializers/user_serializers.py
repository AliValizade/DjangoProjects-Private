from rest_framework import serializers
from ..models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    job_pollution_level = serializers.ChoiceField(
        choices=User.POLLUTION_LEVEL_CHOICES)
    job_category = serializers.ChoiceField(
        choices=User.JOB_TYPE_CHOICES)
    taste_sensitivity = serializers.ChoiceField(
        choices=User.TASTE_SENSITIVITY_CHOICES)
    gender = serializers.ChoiceField(
        choices=User.GENDER_CHOICE)
    class Meta:
        model = User
        fields = ('phone_number', 'email', 'fullname', 'job_pollution_level', 'job_category', 'seasonal_allergy',
                  'taste_sensitivity', 'date_of_birth', 'gender', 'disease', 'password')
        
        
        
    # def validate_phone_number(self, value):
    #     if User.objects.filter(phone_number=value).exists:
    #         raise serializers.ValidationError("شماره تلفن تکراری می باشد ")
    #     return value
    
    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists:
    #         raise serializers.ValidationError('ایمیل تکراری می باشد')
    #     return value
    
class VerifyOtpCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()


class LoginByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class LoginByPhoneNumber(serializers.Serializer):
    phone_number = serializers.CharField()
    
class UserProfileSerializer(serializers.ModelSerializer):
    job_pollution_level = serializers.ChoiceField(choices=User.POLLUTION_LEVEL_CHOICES)
    job_category = serializers.ChoiceField(choices=User.JOB_TYPE_CHOICES)
    taste_sensitivity = serializers.ChoiceField(choices=User.TASTE_SENSITIVITY_CHOICES)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICE)

    phone_number = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = (
            'phone_number', 'email', 'fullname', 'job_pollution_level',
            'job_category', 'seasonal_allergy', 'taste_sensitivity', 
            'date_of_birth', 'gender', 'disease'
        )
