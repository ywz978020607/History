# Generated by Django 2.2.7 on 2021-08-02 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0046_auto_20210802_1614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='productname',
            new_name='name',
        ),
    ]
