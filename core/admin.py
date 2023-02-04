from django.contrib import admin

from core.models import ActivityType, Activity


# Register your models here.
@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    readonly_fields = ('participants', 'created_at', 'updated_at', )
