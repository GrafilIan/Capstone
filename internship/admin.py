from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import intern


class CustomUserAdmin(UserAdmin):
    model = intern
    list_display = ["email", "username",]


admin.site.register(intern, CustomUserAdmin)

# Register your models here.
