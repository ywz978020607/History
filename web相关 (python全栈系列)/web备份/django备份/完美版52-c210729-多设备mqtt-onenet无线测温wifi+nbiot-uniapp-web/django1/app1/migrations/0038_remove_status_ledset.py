# Generated by Django 2.2.7 on 2021-05-14 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0037_auto_20210514_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='ledset',
        ),
    ]
