# Generated by Django 4.2.6 on 2023-10-16 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]