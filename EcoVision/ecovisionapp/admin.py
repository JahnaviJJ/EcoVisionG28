from django.contrib import admin
from .models import Post
from .models import Event


admin.site.register(Post)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organizer')
    search_fields = ('title', 'description', 'location')
    list_filter = ('date',)