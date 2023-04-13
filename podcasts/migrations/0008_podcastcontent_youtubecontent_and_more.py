# Generated by Django 4.1.7 on 2023-04-09 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0007_episode'),
    ]

    operations = [
        migrations.CreateModel(
            name='PodcastContent',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='podcasts.content')),
                ('rss', models.URLField()),
            ],
            bases=('podcasts.content',),
        ),
        migrations.CreateModel(
            name='YoutubeContent',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='podcasts.content')),
                ('channel_id', models.CharField(max_length=100)),
                ('upload_id', models.CharField(max_length=100)),
            ],
            bases=('podcasts.content',),
        ),
        migrations.RemoveField(
            model_name='content',
            name='content_type',
        ),
    ]