# Generated by Django 4.2.13 on 2025-07-11 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MP3File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('artist', models.CharField(blank=True, max_length=255, null=True)),
                ('album', models.CharField(blank=True, max_length=255, null=True)),
                ('genre', models.CharField(blank=True, max_length=255, null=True)),
                ('artwork', models.ImageField(blank=True, null=True, upload_to='artwork/')),
                ('downloaded_file', models.FileField(blank=True, null=True, upload_to='mp3_files/')),
            ],
        ),
    ]
