from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from tuitions.models import Application  
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
        
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Match"})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already Exists"})
        
        account = User(username = username, email = email, first_name = first_name, last_name = last_name)
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()
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

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'applied_tuitions']

    def get_applied_tuitions(self, user):
        applications = Application.objects.filter(tutor=user)
        return AppliedTuitionSerializer(applications, many=True).data