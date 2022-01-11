from django.contrib import admin, messages
from .models import CustomTag, Tagged, CustomAnswerTag, AnswerTagged
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(CustomTag)
class CustomTagAdmin(ImportExportModelAdmin):
    list_display = ("name", "slug")
    list_per_page = 50
    # raw_id_fields = ("similar_tag",)
    list_filter = ["featured"]
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ["name"]}
    actions = ["mark_featured", "mark_not_featured"]

    def mark_featured(self, request, queryset):
        rows_updated = queryset.update(featured=True)
        if rows_updated == 1:
            message_bit = '1 items was'
        else:
            message_bit = f"{rows_updated} items were"
        self.message_user(request, f"{message_bit} marked as featured.",
                          level=messages.SUCCESS)
    mark_featured.short_description = 'Mark selected items as featured'
    mark_featured.allowed_permissions = ('change',)

    def mark_not_featured(self, request, queryset):
        rows_updated = queryset.update(featured=False)
        if rows_updated == 1:
            message_bit = '1 items was'
        else:
            message_bit = f"{rows_updated} items were"
        self.message_user(request, f"{message_bit} marked as not featured.",
                          level=messages.SUCCESS)
    mark_not_featured.short_description = 'Mark selected items as not featured'
    mark_not_featured.allowed_permissions = ('change', )


@admin.register(Tagged)
class TaggedAdmin(ImportExportModelAdmin):
    list_display = ("id", "content_type", "object_id", "tag", "timestamp")
    list_filter = ("content_type", "tag", "timestamp")


@admin.register(CustomAnswerTag)
class CustomAnswerTagAdmin(ImportExportModelAdmin):
    list_display = ("name", "slug")
    list_per_page = 50
    # raw_id_fields = ("similar_tag",)
    list_filter = ["featured"]
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ["name"]}
    actions = ["mark_featured", "mark_not_featured"]

    def mark_featured(self, request, queryset):
        rows_updated = queryset.update(featured=True)
        if rows_updated == 1:
            message_bit = '1 items was'
        else:
            message_bit = f"{rows_updated} items were"
        self.message_user(request, f"{message_bit} marked as featured.",
                          level=messages.SUCCESS)
    mark_featured.short_description = 'Mark selected items as featured'
    mark_featured.allowed_permissions = ('change',)

    def mark_not_featured(self, request, queryset):
        rows_updated = queryset.update(featured=False)
        if rows_updated == 1:
            message_bit = '1 items was'
        else:
            message_bit = f"{rows_updated} items were"
        self.message_user(request, f"{message_bit} marked as not featured.",
                          level=messages.SUCCESS)
    mark_not_featured.short_description = 'Mark selected items as not featured'
    mark_not_featured.allowed_permissions = ('change', )

@admin.register(AnswerTagged)
class AnswerTaggedAdmin(ImportExportModelAdmin):
    list_display = ("id", "content_type", "object_id", "tag", "timestamp")
    list_filter = ("content_type", "tag", "timestamp")
