from django.contrib import admin
from .models import User, Category, TourPackage, Resort, Booking, Enquiry, Review, HeroBanner, SeasonalBanner, Contact, ClientReview
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Customizing User admin to display more information
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_admin', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
    )

# Category model display
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_featured', 'card_image_tag', 'meta_title']
    list_filter = ['is_featured', 'parent']
    search_fields = ['name', 'meta_title', 'meta_description']
    readonly_fields = ['card_image_tag']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'parent', 'is_featured', 'parent_choice')
        }),
        ('Images', {
            'fields': ('banner_image_desktop', 'banner_image_mobile', 'card_image', 'card_image_tag')
        }),
        ('Content', {
            'fields': ('short_description', 'long_description', 'tittle_first', 'tittle_second', 'content_first', 'content_second')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'description': 'Add meta title and description for SEO purposes.'
        }),
    )

    def card_image_tag(self, obj):
        if obj.card_image:
            return format_html('<img src="{}" width="100" height="60" />', obj.card_image.url)
        return "-"
    card_image_tag.short_description = "Card Image"

# TourPackage model display
class TourPackageAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'parent_choice', 'price',
        'days', 'nights', 'get_duration', 'location',
        'image_tag', 'is_featured', 'meta_title', 'meta_description',
        'created_at', 'updated_at'
    )
    search_fields = ('title', 'location')
    list_filter = ('parent_choice', 'is_featured', 'category')
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'tags', 'category', 'parent_choice', 'is_featured')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'description', 'itinerary')
        }),
        ('Media', {
            'fields': ('image_desktop', 'image_mobile', 'card_image', 'image_tag')
        }),
        ('SEO / Meta', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Additional Info', {
            'fields': ('location', 'price', 'days', 'nights')
        }),
    )

    readonly_fields = ('image_tag',)  # <-- Fixed here

    def image_tag(self, obj):
        if obj.image_desktop and hasattr(obj.image_desktop, 'url'):
            return format_html('<img src="{}" width="100" height="100" />', obj.image_desktop.url)
        return "No Image"
    image_tag.short_description = 'Image Preview'

    def get_duration(self, obj):
        days = obj.days or 0
        nights = obj.nights or 0
        return f"{days} days {nights} nights"
    get_duration.short_description = 'Duration'


# Resort model display
class ResortAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price', 'available_rooms', 'image_tag')
    search_fields = ('name', 'location')
    list_filter = ('location',)
    ordering = ('-price',)

    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" />', obj.image.url)

# Booking model display
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking_type', 'status', 'checkin', 'checkout', 'guests')
    search_fields = ('user__username', 'booking_type')
    list_filter = ('status', 'booking_type')
    ordering = ('-checkin',)

# Enquiry model display
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_number', 'related_package', 'created_at')
    search_fields = ('name', 'email', 'contact_number')
    ordering = ('-created_at',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'destination', 'contact_number', 'email', 'message', 'created_at')
    search_fields = ('full_name', 'destination', 'contact_number', 'email')
    ordering = ('-created_at',)

# Review model display
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'package', 'resort', 'created_at')
    search_fields = ('user__username', 'package__title', 'resort__name')
    list_filter = ('rating',)
    ordering = ('-created_at',)

@admin.register(ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('created_at',)

# Register models with custom admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(TourPackage, TourPackageAdmin)
admin.site.register(Resort, ResortAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Review, ReviewAdmin)

admin.site.register(HeroBanner)
admin.site.register(SeasonalBanner)