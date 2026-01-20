from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ['image', 'order']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'property_type', 'sale_type', 'price', 'owner', 'is_active', 'created_at']
    list_filter = ['property_type', 'sale_type', 'is_active', 'created_at']
    search_fields = ['title_en', 'title_ar', 'location_en', 'location_ar', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PropertyImageInline]
    
    fieldsets = (
        ('Owner', {
            'fields': ('owner', 'phone')
        }),
        ('English Content', {
            'fields': ('title_en', 'description_en', 'location_en')
        }),
        ('Arabic Content', {
            'fields': ('title_ar', 'description_ar', 'location_ar')
        }),
        ('Property Details', {
            'fields': ('property_type', 'sale_type', 'price')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['property__title_en', 'property__title_ar']
