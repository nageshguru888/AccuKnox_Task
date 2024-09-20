from django.contrib import admin
from .models import User, FriendRequest, Friend

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('is_active', 'is_staff')  # Fields that cannot be edited directly

    def save_model(self, request, obj, form, change):
        # Custom save logic can be added here if needed
        super().save_model(request, obj, form, change)

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('sender__email', 'receiver__email', 'status')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend')
    search_fields = ('user__email', 'friend__email')
    ordering = ('user',)
