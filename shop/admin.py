from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Address, Category, Product

UserAdmin.list_display += ('notify', )
UserAdmin.list_filter += ('notify', )
UserAdmin.fieldsets += (('notify', {'fields': ('notify', )}), )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'street', 'country', 'code']


    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category',
                    'price', 'available', 'created', 'updated']
    list_filter = ['category', 'available']
    list_editable = ['price', 'available']
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name', )}
