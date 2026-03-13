from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Skill, UserTeaches, ExchangeRequest


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'division', 'date_joined')
    list_filter = ('division', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category',)


@admin.register(UserTeaches)
class UserTeachesAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'available_time')
    list_filter = ('skill__category', 'available_time')
    search_fields = ('user__first_name', 'user__username', 'skill__name')


@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'receiver', 'skill', 'offering_skill', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('requester__first_name', 'receiver__first_name', 'skill__name')
    date_hierarchy = 'created_at'
