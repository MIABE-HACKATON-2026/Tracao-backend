from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from user.models import TracaoUser, Profile



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "profile_picture", "id_picture"]


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = TracaoUser
        fields = ["email", "first_name", "last_name","phone_number","country","city"]

    

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = TracaoUser
        fields = ["email", "first_name", "last_name","phone_number","country","city","is_transporter","is_producer"]

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    list_display = ["email", "first_name", "last_name", "phone_number","country","city","is_transporter","is_producer","created_at","updated_at"]
    list_filter = ["is_transporter", "is_producer","is_superuser"]
    
    # Fieldsets for the change user form
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "phone_number","country","city"]}),
        ("Permissions", {"fields": ["is_transporter", "is_producer", "is_staff", "is_superuser", "groups", "user_permissions"]}),
    ]
    
    # Fieldsets for the add user form
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "last_name","phone_number","country","city", "is_transporter","is_producer","is_staff","is_superuser", "password"],
            },
        ),
    ]
    
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]
    filter_horizontal = []

# Register the new UserAdmin
admin.site.register(TracaoUser, UserAdmin)


