# Generated by Django 4.0.4 on 2022-05-17 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0002_glasses_json_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glasses',
            name='json_data',
            field=models.JSONField(default={}, verbose_name='JSON data'),
        ),
    ]
