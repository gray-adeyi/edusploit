from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, StudentAdditionalInformation


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("identifier", "is_staff", "is_active")
    list_filter = ("identifier", "is_staff", "is_active")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "identifier",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "identifier",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("identifier",)
    ordering = ("identifier",)


admin.site.register(User, UserAdmin)
admin.site.register(StudentAdditionalInformation)
