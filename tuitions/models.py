from django.db import models
from django.conf import settings

class Tuition(models.Model):
    title = models.CharField(max_length=255)
    student_class = models.CharField(max_length=50)
    subject = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
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

class Review(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)