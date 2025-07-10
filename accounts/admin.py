from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from tuitions.models import Application

admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    readonly_fields = ('tuition_history',)

    fieldsets = UserAdmin.fieldsets + (
        ('Tuition History', {
            'fields': ('tuition_history',),
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

admin.site.register(User, CustomUserAdmin)
