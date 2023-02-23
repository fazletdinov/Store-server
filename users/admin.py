from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from products.admin import BasketAdmin
from users.forms import UserChangeForm, UserCreationForm
from users.models import CustomUser, EmailVerification


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone', 'is_admin', 'is_active', 'is_verify')
    inlines = (BasketAdmin,)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(EmailVerification)
class EmailVerification(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
