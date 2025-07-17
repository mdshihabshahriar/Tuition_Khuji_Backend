from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from tuitions.models import Application
from accounts.models import UserProfile,TutorProfile

admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name','phone','is_staff', 'user_type_display')
    readonly_fields = ('tuition_history', 'user_type_display','phone')

    fieldsets = UserAdmin.fieldsets + (
        ('Tuition History', {
            'fields': ('tuition_history',),
        }),
        ('User Info', {
            'fields': ('user_type_display','phone'),
        }),
    )

    def tuition_history(self, obj):
        applications = Application.objects.filter(tutor=obj).select_related('tuition')
        if not applications.exists():
            return "No tuition applied"
        
        lines = []
        for app in applications:
            status = "✅ Selected" if app.is_selected else "❌ Not Selected"
            lines.append(f"• {app.tuition.title} – {status}")
        
        return "\n".join(lines)

    tuition_history.short_description = "Tuition History"

    def user_type_display(self, obj):
        try:
            return obj.userprofile.user_type
        except UserProfile.DoesNotExist:
            return "N/A"

    user_type_display.short_description = "User Type"
    
    def phone(self, obj):
        try:
            return obj.userprofile.phone
        except UserProfile.DoesNotExist:
            return "N/A"
    phone.short_description = "Phone Number"

admin.site.register(User, CustomUserAdmin)

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'user_type', 'phone']

@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ['profile', 'education', 'department','preferred_subjects']
