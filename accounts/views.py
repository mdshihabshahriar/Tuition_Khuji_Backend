from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny

class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/api/accounts/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html',{'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            return Response("Check your email for confirmation")
        return Response(serializer.errors)
    
def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
class UserLoginApiView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username = username, password = password)
            
            if user:
                token, _ = Token.objects.get_or_create(user = user)
                print(token)
                print(_)
                login(request,user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)
    
class UserLogoutApiView(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.PasswordChangeSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if not user.check_password(old_password):
                return Response({'error': 'Old password is incorrect.'}, status=400)

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully.'})
        return Response(serializer.errors, status=400)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.UserProfileSerializer(user)
        return Response(serializer.data)