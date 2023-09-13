from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import intern
from .models import Announcement

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = intern
    list_display = ["email", "username",]


admin.site.register(intern, CustomUserAdmin)

# Register your models here.
