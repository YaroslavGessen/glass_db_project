import os

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from import_export import resources


class Vehicles(models.Model):
    v_number = models.PositiveIntegerField(unique=True, blank=False, verbose_name='Vehicle NUM')
    v_manufacture = models.CharField(max_length=30, unique=False, blank=False, verbose_name='Manufacture')
    v_model = models.CharField(max_length=50, blank=True, null=True, verbose_name='Model')
    v_date_of_prod = models.DateField(blank=False, verbose_name='Date of prod.')

    def __str__(self):
        self.v_number = str(self.v_number)
        return self.v_number

    class Meta:
        db_table = "vehicles"
        verbose_name_plural = 'Vehicles'


class Glasses(models.Model):
    g_model = models.ForeignKey(Vehicles, on_delete=models.CASCADE, verbose_name='Auto ID')
    g_source = models.CharField(max_length=30, blank=True, null=True, verbose_name='Source of data')
    g_damage_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='Type of damage')
    g_damage_side = models.CharField(max_length=30, blank=True, null=True, verbose_name='Damage side')
    g_nak = models.FloatField(default=0, blank=True, null=True, verbose_name='NaK')
    g_mgk = models.FloatField(default=0, blank=True, null=True, verbose_name='MsK')
    g_alk = models.FloatField(default=0, blank=True, null=True, verbose_name='AlK')
    g_sik = models.FloatField(default=0, blank=True, null=True, verbose_name='SiK')
    g_sk = models.FloatField(default=0, blank=True, null=True, verbose_name='S K')
    g_cik = models.FloatField(default=0, blank=True, null=True, verbose_name='CiK')
    g_kka = models.FloatField(default=0, blank=True, null=True, verbose_name='KKA')
    g_kkb = models.FloatField(default=0, blank=True, null=True, verbose_name='KKB')
    g_caka = models.FloatField(default=0, blank=True, null=True, verbose_name='CaKA')
    g_cakb = models.FloatField(default=0, blank=True, null=True, verbose_name='CaKB')
    g_tik = models.FloatField(default=0, blank=True, null=True, verbose_name='TiK')
    g_crk = models.FloatField(default=0, blank=True, null=True, verbose_name='CrK')
    g_mnk = models.FloatField(default=0, blank=True, null=True, verbose_name='MsK')
    g_fek = models.FloatField(default=0, blank=True, null=True, verbose_name='FeK')
    g_coka = models.FloatField(default=0, blank=True, null=True, verbose_name='CoK')
    g_cuka = models.FloatField(default=0, blank=True, null=True, verbose_name='CuKA')
    g_cukb = models.FloatField(default=0, blank=True, null=True, verbose_name='CuKB')
    g_znka = models.FloatField(default=0, blank=True, null=True, verbose_name='ZnKA')
    g_znkb = models.FloatField(default=0, blank=True, null=True, verbose_name='ZnKB')
    g_srk = models.FloatField(default=0, blank=True, null=True, verbose_name='SrK')

    class Meta:
        db_table = "glasses"
        verbose_name_plural = 'Glasses'


class Vectors(models.Model):
    v_source = models.CharField(max_length=30, blank=True, null=True, verbose_name='Source of data')
    json_data = models.JSONField(null=True, verbose_name='JSON data')

    class Meta:
        db_table = "vectors"
        verbose_name_plural = 'Vectors'


class CustomUser(AbstractUser):
    image = models.ImageField(default='img/default.png', upload_to='profile_pics')
    is_viewer = models.BooleanField(default=True)
    is_editor = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} Profile'

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class VehicleResource(resources.ModelResource):
    class Meta:
        model = Vehicles


