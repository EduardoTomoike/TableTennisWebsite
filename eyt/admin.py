from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Video, PlayerProfile, CoachProfile, VideoReview, VirtualCoachingSession, Payment, CoachReview

# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('usatt_number', 'rating', 'location', 'birth_date', 'specialization', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('usatt_number', 'rating', 'location', 'birth_date', 'specialization', 'role')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Video)
admin.site.register(PlayerProfile)
admin.site.register(CoachProfile)
admin.site.register(VideoReview)
admin.site.register(VirtualCoachingSession)
admin.site.register(Payment)
admin.site.register(CoachReview)
