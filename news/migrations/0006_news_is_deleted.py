# Generated by Django 3.0.5 on 2020-04-24 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_news_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
