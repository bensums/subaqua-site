from django.contrib import admin
from events.models import Event, EventCategory

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class EventCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)

