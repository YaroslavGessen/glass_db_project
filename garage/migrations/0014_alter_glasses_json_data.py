# Generated by Django 4.0.4 on 2022-05-18 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0013_alter_glasses_json_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glasses',
            name='json_data',
            field=models.JSONField(verbose_name='JSON data'),
        ),
    ]