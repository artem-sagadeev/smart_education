# Generated by Django 3.0.8 on 2020-07-22 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_constructor', '0011_auto_20200719_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='code',
            field=models.IntegerField(default=10000000, unique=True),
        ),
    ]
