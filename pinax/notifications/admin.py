from django.contrib import admin

from .models import NoticeType, NoticeQueueBatch, NoticeSetting, Notice


class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ["label", "display", "description", "default"]


class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "notice_type", "medium", "scoping", "send"]


class NoticeAdmin(admin.ModelAdmin):
    list_display = ["id", "recipient", "notice_type", "unseen", "updated_on"]
    list_filter = ("notice_type", "updated_on",)
    readonly_fields = ("id", "recipient", "sender", "notice_type", "updated_on",)

admin.site.register(NoticeQueueBatch)
admin.site.register(NoticeType, NoticeTypeAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
