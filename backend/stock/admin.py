from django.contrib import admin

from .models import Category, Manufacturer, Product, Stock, User


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "license")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_disabled", "created_at")
    list_filter = ("role", "is_disabled")
    search_fields = ("username", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "manufacturer",
        "category",
        "made_at_date",
        "expiration_date",
    )
    list_filter = ("category", "manufacturer")
    search_fields = ("name",)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "qty", "user", "created_date")
    list_filter = ("created_date",)
