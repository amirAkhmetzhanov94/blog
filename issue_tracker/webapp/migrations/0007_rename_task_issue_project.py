# Generated by Django 3.2.7 on 2021-10-15 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_rename_task_id_issue_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='task',
            new_name='project',
        ),
    ]
