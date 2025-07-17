# from django.contrib import admin
# from .models import Tuition, Application, Review

# @admin.register(Tuition)
# class TuitionAdmin(admin.ModelAdmin):
#     list_display = ['title', 'student_class', 'location', 'is_available']
#     list_filter = ['student_class', 'is_available']


# class ApplicationAdmin(admin.ModelAdmin):
#     list_display = ('tutor', 'tuition', 'is_selected')
#     list_filter = ('tuition', 'is_selected')  

# admin.site.register(Application, ApplicationAdmin)


# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['application', 'rating', 'created_at']
    
from django.contrib import admin
from .models import Tuition, Application, Review

@admin.register(Tuition)
class TuitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'student_class', 'location', 'posted_by','is_available']
    list_filter = ['student_class', 'is_available']
    search_fields = ['title', 'subject', 'location']
    ordering = ['-created_at']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'tuition', 'is_selected', 'applied_at')
    list_filter = ('is_selected', 'tuition')
    search_fields = ['tutor__username', 'tuition__title']
    ordering = ['-applied_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['application__tutor__username', 'reviewer__username', 'comment']
    ordering = ['-created_at']
