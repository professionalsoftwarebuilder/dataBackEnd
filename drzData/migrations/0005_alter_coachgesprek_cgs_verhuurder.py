# Generated by Django 3.2.5 on 2022-08-09 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drzData', '0004_auto_20220809_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachgesprek',
            name='cgs_Verhuurder',
            field=models.CharField(blank=True, help_text='Naam van verhuurder of woningbouwcooperatie', max_length=85, null=True, verbose_name='Naam verhuurder'),
        ),
    ]