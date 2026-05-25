from django.contrib import admin
from .models import BrandProfile

@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'niche', 'city', 'user')
    search_fields = ('brand_name', 'city')
    list_filter = ('niche',)