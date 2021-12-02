from modeltranslation.translator import translator, TranslationOptions
from webapp.models import Type, Status, Issue, Project


class TypeTranslationOptions(TranslationOptions):
    fields = ('title',)


class StatusTranslationOptions(TranslationOptions):
    fields = ('title',)


class IssueTranslationOptions(TranslationOptions):
    fields = ('summary', 'description')


class ProjectTranslationOptions(TranslationOptions):
    fields = ('project_name', 'project_summary')


translator.register(Type, TypeTranslationOptions)
translator.register(Status, StatusTranslationOptions)
translator.register(Issue, IssueTranslationOptions)
translator.register(Project, ProjectTranslationOptions)
