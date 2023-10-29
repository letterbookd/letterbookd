# Generated by Django 4.2.6 on 2023-10-29 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_librarybook_tracking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarybook',
            name='tracking_status',
            field=models.IntegerField(choices=[(1, 'Finished Reading'), (2, 'Currently Reading'), (3, 'On Hold'), (4, 'Planning to Read'), (5, 'Dropped')], default=0),
        ),
    ]