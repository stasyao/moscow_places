# Generated by Django 3.2.7 on 2021-10-23 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0016_auto_20211023_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='priority',
            field=models.PositiveIntegerField(blank=True, db_index=True, default=0),
        ),
    ]
