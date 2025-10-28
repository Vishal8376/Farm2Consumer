from django.contrib import admin
from .models import User, Product, Order, CartItem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# -------------------------------
# Custom User Admin
# -------------------------------
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


# -------------------------------
# Product Admin
# -------------------------------
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'price', 'quantity', 'location', 'created_at')
    list_filter = ('location', 'farmer')
    search_fields = ('name', 'farmer__email')


# -------------------------------
# Order Admin
# -------------------------------
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__email', 'product__name')


# -------------------------------
# Cart Admin
# -------------------------------
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    search_fields = ('user__email', 'product__name')


# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem, CartItemAdmin)