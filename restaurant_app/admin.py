from django.contrib import admin
from .models import Category, Dish, Review, Order, DishesinOrder

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_popular')
    list_filter = ('category', 'is_available', 'is_popular')
    search_fields = ('name', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish', 'rating', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'rating')
    search_fields = ('user__username', 'comment')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Схвалити обрані відгуки"
@admin.register(DishesinOrder)
class DishesinOrderInline(admin.TabularInline):
    model = DishesinOrder
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'payment_method')
    inlines = [DishesinOrderInline]