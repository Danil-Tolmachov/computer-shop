from django.contrib import admin

from register.models import ShopUser


class ShopUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'get_active_orders_count', 'is_active')


admin.site.register(ShopUser, ShopUserAdmin)
