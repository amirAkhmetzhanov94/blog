from django.core.validators import BaseValidator
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class MaxValueValidator(BaseValidator):
    message = "Value %(value)s has length %(show_value)d. " \
              "Length should be less than %(limit_value)d"

    def clean(self, x):
        return len(x)

    def compare(self, a, b):
        return a > b


@deconstructible
class MinValueValidator(BaseValidator):
    message = "Value %(value)s has length %(show_value)d. " \
              "Min Length should be more than %(limit_value)d"

    def clean(self, x):
        return len(x)

    def compare(self, a, b):
        return a < b


class Type(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name='Title')

    def __str__(self):
        return f'{self.title}'


class Status(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name='Title')

    def __str__(self):
        return f'{self.title}'


class Issue(models.Model):
    summary = models.CharField(max_length=30, validators=[MaxValueValidator(30)], null=False, blank=False,
                               verbose_name='Summary')
    description = models.TextField(max_length=2000, validators=[MinValueValidator(100)], blank=True, null=True,
                                   verbose_name='Description')
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, verbose_name='Status', related_name='issues')
    type = models.ManyToManyField('webapp.Type', related_name='issues')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='Creation time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update time')
    task_id = models.ForeignKey('Project', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.summary} ({self.status}, {self.type.get()})'


class Project(models.Model):
    start_date = models.DateField()
    finish_date = models.DateField(blank=True)
    project_name = models.CharField(max_length=30)
    project_summary = models.TextField()

    def __str__(self):
        return f'{self.project_name}'
