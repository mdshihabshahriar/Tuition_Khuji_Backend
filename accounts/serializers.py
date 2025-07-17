from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from tuitions.models import Application  
from django.contrib.auth import get_user_model
from .models import UserProfile,TutorProfile

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True)
    confirm_password = serializers.CharField(required = True)
    user_type = serializers.ChoiceField(choices=[('student', 'Student/Parent'), ('tutor', 'Tutor')])
    phone = serializers.CharField(required=True)
     
    class Meta:
        model = User
        fields = ['user_type','username','first_name','last_name','email','phone','password','confirm_password']
       
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
     
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        user_type = self.validated_data['user_type']
        phone = self.validated_data['phone']
        
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Match"})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already Exists"})
        
        account = User(username = username, email = email, first_name = first_name, last_name = last_name)
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()
    
        UserProfile.objects.create(user=account, user_type=user_type)
        
        return account

    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        validate_password(data['new_password'])
        return data
    
class AppliedTuitionSerializer(serializers.ModelSerializer):
    tuition_title = serializers.CharField(source='tuition.title', read_only=True)
    tuition_id = serializers.IntegerField(source='tuition.id', read_only=True)
    is_selected = serializers.BooleanField()

    class Meta:
        model = Application
        fields = ['tuition_id', 'tuition_title', 'is_selected']

class UserProfileSerializer(serializers.ModelSerializer):
    applied_tuitions = serializers.SerializerMethodField()
    tutor_profile = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'user_type', 'applied_tuitions', 'tutor_profile'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.instance
        if isinstance(user, User) and hasattr(user, 'userprofile'):
            if user.userprofile.user_type == 'student':
                self.fields.pop('applied_tuitions')
                self.fields.pop('tutor_profile')

    def get_user_type(self, user):
        try:
            return user.userprofile.user_type
        except:
            return None

    def get_applied_tuitions(self, user):
        applications = Application.objects.filter(tutor=user)
        return AppliedTuitionSerializer(applications, many=True).data

    def get_tutor_profile(self, user):
        try:
            tutor_profile = TutorProfile.objects.get(profile=user.userprofile)
            return TutorProfileSerializer(tutor_profile).data
        except TutorProfile.DoesNotExist:
            return None

    
class TutorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorProfile
        fields = ['education', 'department', 'preferred_subjects', 'gender']
