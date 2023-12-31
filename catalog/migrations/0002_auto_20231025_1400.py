# Generated by Django 4.2.5 on 2023-10-25 07:00

from django.db import migrations
from django.core.management import call_command


class Migration(migrations.Migration):
    def load_my_initial_data(apps, schema_editor):
        call_command("loaddata", "books_data.json")

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]
