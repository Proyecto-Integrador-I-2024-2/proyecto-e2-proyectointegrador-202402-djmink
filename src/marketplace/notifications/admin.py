from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Notification

class AbstractNotifyAdmin(admin.ModelAdmin):
    raw_id_fields = ('destiny',)
    list_display = ('level', 'actor', 'verb', 'read', 'public')
    list_filter = ('level', 'read', 'public')

    def get_queryset(self, requests):
        qs = super(AbstractNotifyAdmin, self).get_queryset(requests)
        return qs.prefetch_related('actor')

admin.site.register(Notification, AbstractNotifyAdmin)