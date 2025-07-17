from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPES = (
        ('student', 'Student/Parent'),
        ('tutor', 'Tutor'),
    )
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES,default = 'student')
    phone = models.CharField(max_length=20, default = 'N/A')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.user_type}"
    
class TutorProfile(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    education = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    preferred_subjects = models.TextField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    
    def __str__(self):
        return self.profile.user.username