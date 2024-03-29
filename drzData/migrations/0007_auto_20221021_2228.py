# Generated by Django 3.2.15 on 2022-10-21 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drzData', '0006_auto_20220809_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='vraag',
            name='vrg_Afhandelaren',
            field=models.ManyToManyField(blank=True, help_text='Medewerkers die vraag behandelen', related_query_name='afhandelaren_related', to=settings.AUTH_USER_MODEL, verbose_name='Afhandelaren'),
        ),
        migrations.AddField(
            model_name='vraag',
            name='vrg_Exposanten',
            field=models.ManyToManyField(blank=True, help_text='Aan deze vraag gekoppelde exposanten', related_query_name='exposanten_related', to='drzData.Exposant', verbose_name='Exposanten'),
        ),
        migrations.AlterField(
            model_name='coachgesprek',
            name='cgs_AdviesContact',
            field=models.OneToOneField(default=1, help_text='Kies bijbehorende adviescontact', on_delete=django.db.models.deletion.CASCADE, to='drzData.adviescontact', verbose_name='adviescontact'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coachgesprek',
            name='cgs_Problemen_Gng',
            field=models.CharField(blank=True, choices=[('S', 'Schimmel'), ('V', 'Vocht'), ('G', 'Geluid'), ('N', 'Geen')], help_text='Constateerd u problemen in de gang?', max_length=1, null=True, verbose_name='Problemen gang'),
        ),
        migrations.AlterField(
            model_name='coachgesprek',
            name='cgs_Problemen_K',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('S', 'Schimmel'), ('V', 'Vocht'), ('G', 'Geluid'), ('N', 'Geen')], help_text='Constateerd u problemen in de keuken?', max_length=7, null=True, verbose_name='Problemen keuken'),
        ),
        migrations.AlterField(
            model_name='coachgesprek',
            name='cgs_Problemen_Slk',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('S', 'Schimmel'), ('V', 'Vocht'), ('G', 'Geluid'), ('N', 'Geen')], help_text='Constateerd u problemen in de slaapkamer?', max_length=7, null=True, verbose_name='Problemen slaapkamer'),
        ),
        migrations.AlterField(
            model_name='coachgesprek',
            name='cgs_Problemen_Wk',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('S', 'Schimmel'), ('V', 'Vocht'), ('G', 'Geluid'), ('N', 'Geen')], help_text='Constateerd u problemen in de woonkamer?', max_length=7, null=True, verbose_name='Problemen woonkamer'),
        ),
        migrations.AlterField(
            model_name='coachgesprek',
            name='cgs_StatusGesprek',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('A', 'Aangemeld'), ('B', 'Gebeld - Ingeplanned'), ('E', 'BevestigingsE-mail verstuurd'), ('G', 'Gesprek geschied'), ('O', 'Advies opgemaakt'), ('F', 'Followup ingeplanned'), ('V', 'Bevestiging followup verstuurd')], help_text='De verschillende statussen in het traject van de coachgesprek', max_length=13, null=True, verbose_name='Status van Coachgesprek'),
        ),
    ]
