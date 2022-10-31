from django.contrib import admin

from register.models import ShopUser


class ShopUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'orders', 'is_moderator', 'is_active')


admin.site.register(ShopUser, ShopUserAdmin)
