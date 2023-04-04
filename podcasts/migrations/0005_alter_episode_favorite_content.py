# Generated by Django 4.1.7 on 2023-04-04 22:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('podcasts', '0004_episode_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='favorite',
            field=models.ManyToManyField(blank=True, default=None, related_name='episode_favorite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.URLField()),
                ('categories', models.TextField()),
                ('link', models.URLField()),
                ('content_type', models.CharField(choices=[('PC', 'Podcast'), ('YT', 'Youtube')], max_length=7)),
                ('favorite', models.ManyToManyField(blank=True, default=None, related_name='content_favorite', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
