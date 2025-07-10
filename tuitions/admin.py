from django.contrib import admin
from .models import Tuition, Application, Review

@admin.register(Tuition)
class TuitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'student_class', 'location', 'is_available']
    list_filter = ['student_class', 'is_available']


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'tuition', 'is_selected')
    list_filter = ('tuition', 'is_selected')  

admin.site.register(Application, ApplicationAdmin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'rating', 'created_at']
    
