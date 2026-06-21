from django.contrib import admin
from django.utils.html import format_html
from .models import StudentRegistration

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 
        'email', 
        'phone_number', 
        'course', 
        'batch', 
        'experience_level', 
        'payment_status',
        'registered_at', 
        'thumbnail_preview',
        'screenshot_preview'
    )
    
    list_editable = (
        'course', 
        'batch', 
        'experience_level',
        'payment_status'
    )
    
    list_filter = (
        'course', 
        'batch', 
        'experience_level',
        'payment_status',
        'registered_at'
    )
    
    search_fields = (
        'full_name', 
        'email', 
        'phone_number'
    )
    
    readonly_fields = (
        'registered_at', 
        'updated_at',
        'thumbnail_preview',
        'screenshot_preview'
    )
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number', 'date_of_birth', 'education')
        }),
        ('Course Preferences', {
            'fields': ('course', 'batch', 'experience_level')
        }),
        ('Student Photo', {
            'fields': ('profile_picture', 'thumbnail_preview')
        }),
        ('Payment Details', {
            'fields': ('payment_status', 'payment_screenshot', 'screenshot_preview')
        }),
        ('Metadata', {
            'fields': ('comments', 'registered_at', 'updated_at'),
            'classes': ('collapse',), # Let comments/date be collapsible
        }),
    )

    actions = ['mark_as_verified', 'mark_as_pending']

    def thumbnail_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 2px solid #6366f1;" />',
                obj.profile_picture.url
            )
        return format_html('<span style="color: #94a3b8; font-style: italic;">No Photo</span>')
    
    thumbnail_preview.short_description = 'User Pic'

    def screenshot_preview(self, obj):
        if obj.payment_screenshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" /></a>',
                obj.payment_screenshot.url,
                obj.payment_screenshot.url
            )
        return format_html('<span style="color: #94a3b8; font-style: italic;">No Proof</span>')
    
    screenshot_preview.short_description = 'Payment Proof'

    def mark_as_verified(self, request, queryset):
        count = 0
        for student in queryset:
            if student.payment_status != 'verified':
                student.payment_status = 'verified'
                student.save()
                count += 1
        if count == 1:
            message_bit = "1 student registration was"
        else:
            message_bit = f"{count} student registrations were"
        self.message_user(request, f"{message_bit} successfully marked as Verified and email confirmation sent.")
    mark_as_verified.short_description = "Mark selected registrations as Verified"

    def mark_as_pending(self, request, queryset):
        count = 0
        for student in queryset:
            if student.payment_status != 'pending':
                student.payment_status = 'pending'
                student.save()
                count += 1
        if count == 1:
            message_bit = "1 student registration was"
        else:
            message_bit = f"{count} student registrations were"
        self.message_user(request, f"{message_bit} successfully marked as Pending Payment.")
    mark_as_pending.short_description = "Mark selected registrations as Pending Payment"



