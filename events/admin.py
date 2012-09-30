from django.contrib import admin
from events.models import Event, EventCategory, RSVP

class RSVPInline(admin.TabularInline):
    model = RSVP
    extra = 0

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = (RSVPInline,)

class EventCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)

