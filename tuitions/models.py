from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Tuition(models.Model):
    title = models.CharField(max_length=255)
    student_class = models.CharField(max_length=50)
    subject = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null = True)
    selected_tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_tuitions')
    
    def __str__(self):
        return f"{self.title}-{self.student_class}-{self.subject}"

class Application(models.Model):
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tuition = models.ForeignKey(Tuition, on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tutor', 'tuition')
        
    def __str__(self):
        return f"{self.tutor} {self.tuition }"

User = get_user_model()

class Review(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE,null = True,blank = True)
    comment = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.application.tuition.title} - {self.application.tutor.username}"