from django.db import models


class Type(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name='Title')

    def __str__(self):
        return f'{self.title}'


class Status(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name='Title')

    def __str__(self):
        return f'{self.title}'


class Issue(models.Model):
    summary = models.CharField(max_length=30, null=False, blank=False, verbose_name='Summary')
    description = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Description')
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, verbose_name='Status', related_name='issues')
    type = models.ManyToManyField('webapp.Type', related_name='issues')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='Creation time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update time')

    def __str__(self):
        return f'{self.summary} ({self.status}, {self.type})'
