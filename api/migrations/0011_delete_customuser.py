# Generated by Django 4.2.6 on 2023-10-17 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
