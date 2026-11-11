from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BaseUser, Cart, CartProduct, Product, ProductTransaction, Transaction


@admin.register(BaseUser)
class BaseUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Extra", {"fields": ("middle_name", "gender", "avatar")}),)


class ProductTransactionInline(admin.TabularInline):
    model = ProductTransaction
    extra = 0


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "created_at")
    inlines = [ProductTransactionInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "stock", "is_active")
    search_fields = ("name", "sku")


admin.site.register(Cart)
admin.site.register(CartProduct)
