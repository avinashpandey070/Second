# Generated by Django 3.0.5 on 2020-04-12 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_main_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main',
            name='about',
            field=models.TextField(),
        ),
    ]