# Generated by Django 4.0.4 on 2022-06-29 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0029_alter_glasses_g_alk_alter_glasses_g_caka_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glasses',
            name='g_damage_side',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Damage side'),
        ),
    ]
