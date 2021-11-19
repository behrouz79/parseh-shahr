from django.contrib import admin
from .models import Category, Product, Image, Comment, Sell


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'stock', 'discounted')
    list_editable = ('amount', 'stock', 'discounted')
    list_filter = ('title', 'amount', 'stock', 'discounted')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Sell)
class SellAdmin(admin.ModelAdmin):
    list_display = ('target', 'count')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'active')
    list_editable = ('active',)

    actions = ('make_active',)

    def make_active(self, request, queryset):
        rows = queryset.update(active=True)
        self.message_user(request, f'{rows} تایید شد.')

    make_active.short_description = 'تایید کردن'


admin.site.register(Image)

