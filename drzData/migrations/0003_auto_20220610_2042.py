# Generated by Django 3.0.5 on 2022-06-10 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drzData', '0002_auto_20220602_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grp_GroupNm', models.CharField(max_length=45, verbose_name='Group')),
                ('grp_Website', models.CharField(blank=True, max_length=240, null=True, verbose_name='Achternaam')),
                ('grp_Notities', models.TextField(blank=True, null=True, verbose_name='Notities')),
            ],
            options={
                'verbose_name_plural': 'Groepen',
            },
        ),
        migrations.AddField(
            model_name='contact',
            name='cnt_Groepen',
            field=models.ManyToManyField(to='drzData.Groep'),
        ),
    ]
