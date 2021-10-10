# Generated by Django 3.2.7 on 2021-10-04 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('description_short', models.CharField(max_length=300, unique=True)),
                ('description_long', models.TextField()),
                ('coordinates', models.JSONField(default=dict)),
            ],
        ),
    ]