# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FriendRequest

# Customizing the User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username',)
    ordering = ('email',)

# Registering the custom User Admin
admin.site.register(User, CustomUserAdmin)

# Customizing the FriendRequest Admin
class FriendRequestAdmin(admin.ModelAdmin):
    model = FriendRequest
    list_display = ('from_user', 'to_user', 'created_at',)
    list_filter = ('from_user', 'to_user', 'created_at',)
    search_fields = ('from_user__email', 'to_user__email',)

# Registering the FriendRequest Admin
admin.site.register(FriendRequest, FriendRequestAdmin)
