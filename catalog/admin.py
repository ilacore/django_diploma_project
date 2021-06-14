from django.contrib import admin

# Register your models here.
from embed_video.admin import AdminVideoMixin
from .models import User, Post, Item

# admin.site.register(User)
"""@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at', 'email', 'password', 'is_enabled')
    list_filter = ('is_enabled',)"""


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ('display_text', 'author', 'created_at', 'is_enabled')
    list_filter = ('author', 'text')
    fieldsets = (
        ('Creation', {
            'fields': ('author', 'created_at')
        }), ('Post Related', {
            'fields': ('text', 'parent')
        }),
        (None, {
            'fields': ('is_enabled',)
        }),
    )


class ItemAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(Item, ItemAdmin)
