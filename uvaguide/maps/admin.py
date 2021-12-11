import json
from django.contrib import admin
from .models import Place, Review

# Register your models here.
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'place', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('content',)

admin.site.register(Place, PlaceAdmin)
admin.site.register(Review, ReviewAdmin)