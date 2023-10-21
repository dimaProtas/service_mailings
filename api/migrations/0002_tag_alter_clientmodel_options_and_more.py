# Generated by Django 4.2.6 on 2023-10-13 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='clientmodel',
            options={'verbose_name_plural': 'Клиент'},
        ),
        migrations.AlterModelOptions(
            name='mailinglistmodel',
            options={'verbose_name_plural': 'Рассылка'},
        ),
        migrations.AlterModelOptions(
            name='messagemodel',
            options={'verbose_name_plural': 'Cообщение'},
        ),
        migrations.RemoveField(
            model_name='clientmodel',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='mailinglistmodel',
            name='tag',
        ),
        migrations.AddField(
            model_name='clientmodel',
            name='tags',
            field=models.ManyToManyField(to='api.tag'),
        ),
        migrations.AddField(
            model_name='mailinglistmodel',
            name='tags',
            field=models.ManyToManyField(to='api.tag'),
        ),
    ]