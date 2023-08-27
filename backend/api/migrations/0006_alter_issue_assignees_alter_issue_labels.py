# Generated by Django 4.2.4 on 2023-08-24 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_githubuser_remove_issue_assigned_to_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignees',
            field=models.ManyToManyField(blank=True, related_name='assigned_issues', to='api.githubuser'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(blank=True, to='api.label'),
        ),
    ]