# Generated by Django 4.2.6 on 2023-10-25 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_text', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now=True)),
                ('last_edited', models.DateTimeField()),
                ('replying_to', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.forumpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reader.reader')),
            ],
        ),
        migrations.CreateModel(
            name='ForumThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('tags', models.CharField(max_length=255)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('initial_post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forum.forumpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reader.reader')),
            ],
        ),
    ]