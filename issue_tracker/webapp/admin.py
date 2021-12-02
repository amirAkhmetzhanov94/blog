from django.contrib import admin
from webapp.models import Type, Status, Issue, Project
from modeltranslation.admin import TranslationAdmin


class TypeAdmin(TranslationAdmin):
    pass


class StatusAdmin(TranslationAdmin):
    pass


class IssueAdmin(TranslationAdmin):
    pass


class ProjectAdmin(TranslationAdmin):
    pass


admin.site.register(Type, TypeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
