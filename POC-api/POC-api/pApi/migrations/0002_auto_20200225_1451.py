# Generated by Django 2.2.10 on 2020-02-25 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='priority',
            field=models.IntegerField(),
        ),
    ]