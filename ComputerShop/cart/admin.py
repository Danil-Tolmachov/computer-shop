from django.contrib import admin

from cart.models import Order, Category, Product, Storage, ProductImage, ProductItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_customer_name', 'date_created', 'status', 'get_products_count', 'get_summary', 'is_paid', 'is_closed')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category_name', 'category_slug', 'get_product_count')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'price', 'get_all_count', 'characteristics', 'is_visible', 'is_available')
    list_filter = ('category', 'is_visible', 'is_available')


class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'product_count', 'get_source', 'get_related_id')


class StorageAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', 'get_positions_count')


admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductItem, ProductItemAdmin)
