# Generated by Django 3.2.7 on 2021-10-23 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0017_alter_image_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='pub_status',
            field=models.CharField(choices=[('D', 'Черновик'), ('P', 'Опубликован')], default='D', max_length=1),
        ),
    ]