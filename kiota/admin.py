from django.contrib import admin
from .models import House, HouseImage, CompanyProfile, ContactMessage


class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 4      
    max_num = 10    


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'whatsapp_number', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title', 'city', 'address')
    list_filter = ('city', 'is_published', 'list_date')
    inlines = [HouseImageInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'price', 'is_published')
        }),
        ('Location Details', {
            'fields': ('address', 'city')
        }),
        ('Property Specs', {
            'fields': ('bedrooms', 'bathrooms', 'sqft')
        }),
        ('Media & Contact', {
            'fields': ('photo_main', 'whatsapp_number')
        }),
    )


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevents more than one company profile from being created
        return not CompanyProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevents accidental deletion of the company identity
        return False

    list_display = ('name', 'email', 'phone')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('name', 'email', 'message', 'created_at')

    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email', 'created_at')
        }),
        ('The Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )

#  Customizing the Dashboard Branding
admin.site.site_header = "Kiota Admin Panel"
admin.site.site_title = "Kiota Portal"
admin.site.index_title = "Welcome to Kiota Management"
