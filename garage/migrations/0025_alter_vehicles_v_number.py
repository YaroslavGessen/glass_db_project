# Generated by Django 4.0.4 on 2022-06-22 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0024_alter_vehicles_v_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='v_number',
            field=models.PositiveIntegerField(verbose_name='Vehicle NUM'),
        ),
    ]
