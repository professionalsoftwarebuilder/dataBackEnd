from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import widgets
from .models import Bezoekreden, WinkelBezoek, Exposant, AdviesContact, Vraag, Contact, Woninggegevens, CoachGesprek
from django.forms import inlineformset_factory

TYPEEXPOSANT_CHS = (
    ('O', 'Bedrijf'),
    ('G', 'Gemeente instelling'),
    ('B', 'Organisatie'),
)

theWidget = forms.TextInput(attrs={'size': '10'})
wdgSmall = forms.TextInput(attrs={'size': '6'})
wdgTextA = forms.Textarea(attrs={'rows': 2, 'cols': 60})
notFld = forms.CharField(widget=wdgTextA, label='Notities', required=False)


class ContactForm(forms.ModelForm):
    cnt_TussenVgsl = forms.CharField(widget=theWidget, label='Tussenvoegsels', required=False)
    cnt_VoorLtrs = forms.CharField(widget=theWidget, label='Voorletters', required=False)
    cnt_Notities = forms.CharField(widget=wdgTextA, label='Notities', required=False)


class AdviesContactForm(forms.ModelForm):
    cnt_TussenVgsl = forms.CharField(widget=theWidget, label='Tussenvoegsels', required=False)
    cnt_VoorLtrs = forms.CharField(widget=theWidget, label='Voorletters', required=False)
    cnt_Notities = forms.CharField(widget=wdgTextA, label='Notities', required=False)

    class Meta:
        model = AdviesContact
        fields = ('cnt_Vastlegger',
                  'cnt_DatVastlegging',
                  'cnt_VoorNm',
                  'cnt_AchterNm',
                  'cnt_TussenVgsl',
                  'cnt_VoorLtrs',
                  'cnt_Notities',
                  'cnt_Type',
                  'cnt_NieuwsBrief',
                  'cnt_Acties',
                  'cnt_Activiteit'
                  )


class AdviesContactFrontForm(forms.ModelForm):
    cnt_TussenVgsl = forms.CharField(widget=theWidget, label='Tussenvoegsels', required=False)
    cnt_VoorLtrs = forms.CharField(widget=theWidget, label='Voorletters', required=False)
    cnt_Notities = forms.CharField(widget=wdgTextA, label='Notities', required=False)
    cnt_DatVastlegging = forms.SplitDateTimeField(widget=AdminSplitDateTime, label='Tijdstip vastgelegd')

    class Meta:
        model = AdviesContact
        fields = ('cnt_Vastlegger',
                  'cnt_DatVastlegging',
                  'cnt_VoorNm',
                  'cnt_AchterNm',
                  'cnt_TussenVgsl',
                  'cnt_VoorLtrs',
                  'cnt_Notities',
                  'cnt_NieuwsBrief',
                  'cnt_Acties',
                  'cnt_Activiteit',
                  )


class ExposantForm(forms.ModelForm):
    grp_GroupNm = forms.CharField(label='Exposant (naam)', max_length=45)
    grp_Notities = notFld
    grp_Type = forms.ChoiceField(label='Type Exposant', choices=TYPEEXPOSANT_CHS)


class AdresForm(forms.ModelForm):
    adr_HuisNr = forms.CharField(widget=wdgSmall, label='Huisnummer', required=False)
    adr_HuisNrToev = forms.CharField(widget=theWidget, label='Toevoeging', required=False)
    # adr_Land = CountryField(multiple=False)
    adr_PostCd = forms.CharField(widget=theWidget, label='Postcode', required=False)
    adr_Notities = forms.CharField(widget=wdgTextA, label='Notities', required=False)


# class AdresGrForm(forms.ModelForm):
#     adg_HuisNr = forms.CharField(widget=wdgSmall, label='Huisnummer', required=False)
#     adg_HuisNrToev = forms.CharField(widget=theWidget, label='Toevoeging', required=False)
#     #adr_Land = CountryField(multiple=False)
#     adg_PostCd = forms.CharField(widget=theWidget, label='Postcode', required=False)
#     adg_Notities = forms.CharField(widget=wdgTextA, label='Notities', required=False)


class NummerForm(forms.ModelForm):
    nmb_Notities = forms.CharField(widget=wdgTextA, label='Notities', required=False,
                                   help_text='Kanttekening bij dit nummer (bijv: meest recent)')


# class NummerGrForm(forms.ModelForm):
#     nmg_Notities = forms.CharField(widget=wdgTextA, label='Notities', required=False, help_text='Kanttekening bij dit nummer (bijv: meest recent)')


class WinkelBezoekForm(forms.ModelForm):
    wbz_TijdStip = forms.SplitDateTimeField(widget=AdminSplitDateTime, label='Tijdstip van bezoek')
    wbz_Bezoeken = forms.ModelMultipleChoiceField(
        queryset=Bezoekreden.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'style': 'list-style-type:none;'}),
        # empty_label='Geen bezoekredenen in systeem aanwezig',
        label='Bezoekreden(en)',
    )
    wbz_Notities = forms.CharField(widget=wdgTextA, label='Notities')

    class Meta:
        model = WinkelBezoek
        fields = ('wbz_TijdStip', 'wbz_Bezoeken', 'wbz_Notities')


class VraagForm(forms.ModelForm):
    #vrg_Tekst = forms.CharField(widget=wdgTextA, label='Vraag tekst', required=False)
    # vrg_TypeVraag = forms.CharField(label='Type vraag', max_length=1, choices=TYPEVRAAG_CHS, blank=True, null=True)
    # vrg_OnderwerpVraag = forms.CharField(label='Onderwerp vraag', max_length=3, choices=ONDERWERPVRAAG_CHS, blank=True, null=True)
    # vrg_StatusVraag = forms.CharField(label='Status vraag', max_length=1, choices=STATUSVRAAG_CHS, blank=True, null=True)

    class Meta:
        model = Vraag
        fields = ('vrg_Tekst', 'vrg_OnderwerpVraag', 'vrg_StatusVraag', 'vrg_TypeVraag')


class WoninggegevensForm(forms.ModelForm):

    class Meta:
        model = Woninggegevens
        fields = ('wng_TypeWoning', 'wng_Bouwjaar', 'wng_Bewoning')


class AdviesContactListForm(forms.ModelForm):

    class Meta:
        model = AdviesContact
        fields = ('cnt_VoorNm', 'cnt_TussenVgsl', 'cnt_AchterNm')



class CoachgesprekForm(forms.ModelForm):
    # cgs_AdviesContact = forms.OneToOneField(AdviesContact, label='Adviescontact', help_text='Kies bijbehorende adviescontact')
    # cgs_AanmeldingWoonCorp = form.CharField(label='Aanmelding Wooncooperatie', choices=AANMELDWOONCORP_CHS, )
    # cgs_AanmeldingZelf = models.CharField('Zelf aangemenld', max_length=2, choices=AANMELDZELF_CHS, blank=True, null=True)
    # cgs_AanmeldAnders = models.TextField('Anders', blank=True, null=True, help_text='Andere reden voor aanmelding')

    def __init__(self, *args, **kwargs):
        super(CoachgesprekForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__ == forms.widgets.Textarea:
                field.widget = wdgTextA

    class Meta:
        model = CoachGesprek
        fields = ('cgs_AdviesContact',
                        'cgs_AanmeldingWoonCorp',
                        'cgs_AanmeldingZelf',
                        'cgs_AanmeldAnders',            # 5 -o- Aanmelding
                        'cgs_IsModemAanw',              # 5 -i- Telf voorbereiding
                        'cgs_TypeCentrVent',
                        'cgs_TypeElektraMeter',
                        'cgs_HuurderInfo',
                        'cgs_DatTijdGesprek',
                        'cgs_WieAanWezig',
                        'cgs_IsWoningToerAangekond',
                        'cgs_EnergieRekBijDeHand',
                        'cgs_ElektraMeter',
                        'cgs_Motivatie',
                        'cgs_MotivatieAnders',          # 15 -o- Telf voorbereiding
                        'cgs_IsDatumTijdBevestigd',     # 16 -i- Afspraakbevestiging
                        'cgs_IsDocsKlaarGelegd',
                        'cgs_IsWonToerHerAangeKond',
                        'cgs_IsInAgendGeplaatst',       # 19 -o- Afspraakbevestiging
                        'cgs_GenomenEnergMaatr',        # 20 -i- Woningcorperatie
                        'cgs_GeplandeEnrgMaatr',
                        'cgs_EnergieLabel',
                        'cgs_BekendeProbl',             # 23 -o- Woningcorperatie
                        'cgs_RedenEnergBesp',           # 24 -i- Wensen bespreken
                        'cgs_RedenEnergBespAnderen',
                        'cgs_ToekomstPlanWoning',
                        'cgs_MetWieHierWonen',
                        'cgs_BudgetKlMaatr',
                        'cgs_IetsGedaanEnrgMaatr',
                        'cgs_AfwijkEnergRek',           # 30 -o- Wensen bespreken
                        'cgs_TypeThermostaat',          # 31 -i- Woonkamer
                        'cgs_TypeRadiatorknop',
                        'cgs_IsAquariumAanw',
                        'cgs_IsAircoAanw',
                        'cgs_TypeRaambekleding_Wk',
                        'cgs_TypeVerlichting_Wk',
                        'cgs_Problemen_Wk',
                        'cgs_OverigOpmerk_Wk',          # 38 -o- Woonkamer
                        'cgs_TypeWasMachGebruik',       # 39 -i- Keuken
                        'cgs_IsKokenMetDeksel',
                        'cgs_TypeKookSysteem',
                        'cgs_IsAfzuigingVrij',
                        'cgs_IsCloseInBoilerAanw',
                        'cgs_AanwApperatuur',
                        'cgs_Problemen_K',
                        'cgs_OverigOpmerk_K',           # 46 -o- Keuken
                        'cgs_IsRadiatorAanw_Gng',       # 47 -i- Gang
                        'cgs_IsBrievenBusAanw_Gng',
                        'cgs_TypeVerlichting_Gng',
                        'cgs_TypeTochtVoorziening_Gng',
                        'cgs_Problemen_Gng',
                        'cgs_OverigOpmerk_Gng',         # 52 -o- Gang
                        'cgs_CVOnderhoud',              # 53 -i- CV ketel
                        'cgs_CVTemperatuur',            # 54 -o- CV ketel
                        'cgs_TypeVerlichting_Slk',      # 55 -i- Slaapkamer
                        'cgs_IsApparatuurStndBy',
                        'cgs_IsVerwarmd',
                        'cgs_IsAircoAanw_Slk',
                        'cgs_TypeBed',
                        'cgs_Problemen_Slk',
                        'cgs_OverigOpmerk_Slk',         # 61 -o- Slaapkamer
                        'cgs_IsTuinVerlAanw',           # 62 -i- Tuin
                        'cgs_IsVijverpompAanw',
                        'cgs_IsTerrasVerwAanw',
                        'cgs_OverigOpmerk_Tn',          # 65 -o- Tuin
                        'cgs_IsTwedeeKoelkAanw',        # 66 -i- Schuur
                        'cgs_OverigOpmerk_Sch',         # 67 -o- Schuur
                        'cgs_BespaarAdviesTekst',)



VraagInlineFormset = inlineformset_factory(
    AdviesContact,
    Vraag,
    form=VraagForm,
    extra=1,
    # max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)

WoninggegevensInlineFormset = inlineformset_factory(
    AdviesContact,
    Woninggegevens,
    form=WoninggegevensForm,
    extra=1,
)
