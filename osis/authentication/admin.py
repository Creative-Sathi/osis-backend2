from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authentication.models import User


class UserModelAdmin(BaseUserAdmin):
    list_display = ["username", "name", "is_admin", "role"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "role"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "name", "role", "password1", "password2"],
            },
        ),
    ]
    
    search_fields = ["username"]
    ordering = ["username", "id"]
    filter_horizontal = []


admin.site.register(User, UserModelAdmin)
