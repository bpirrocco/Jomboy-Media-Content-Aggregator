# Generated by Django 4.1.7 on 2023-04-09 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0008_podcastcontent_youtubecontent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='podcast_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcasts.podcastcontent'),
        ),
    ]
