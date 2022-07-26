from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.urls import reverse

MOTIVATIE_CHS = (
    ('Ml', 'Verlagen maandlasten'),
    ('C', 'Confort verbeteren'),
    ('L', 'Leuke uitdaging'),
    ('G', 'Gezondheid'),
    ('M', 'Iets voor het milieu doen'),
    ('A', 'Niet achter willen blijven'),
    ('Vl', 'Voorop willen lopen'),
)

KEUKENAPPARATUUR_CHS = (
    ('T', 'Thuistap'),
    ('Wk', 'Waterkoker'),
    ('Km', 'Keukenmachine'),
    ('Ka', 'Koffiezetapparaat'),
    ('Br', 'Broodrooster'),
    ('Cg', 'Contact grill'),
)

ENERGIEMETER_CHS = (
    ('G', 'Gewoon'),
    ('S', 'Slimme meter'),
)

TYPEBEDVERWARMING_CHS = (
    ('G', 'Geen'),
    ('W', 'Waterbed'),
    ('E', 'Elektrische deken'),
)

TYPEPROBLEEM_CHS = (
    ('S', 'Schimmel'),
    ('V', 'Vocht'),
    ('G', 'Geluid'),
)

TYPECVKETELONDERHOUD_CHS = (
    ('N', 'Niet'),
    ('P', 'Periodiek'),
)

TYPECENTRALEVENT_CHS = (
    ('G', 'Geen'),
    ('Gf', 'Geforceerd'),
    ('Gb', 'Gebalanceerd'),
)

TYPETOCHTVOORZIENING_CHS = (
    ('G', 'Geen'),
    ('Ts', 'Tochtstrip'),
    ('K', 'Kussen'),
)


TYPEKOOKSYSTEEM_CHS = (
    ('G', 'Gas'),
    ('I', 'Inductie'),
    ('K', 'Keramisch'),
    ('O', 'Oven'),
    ('M', 'Magnetron'),
)

TYPEWASMACHINEGEBRUIK_CHS = (
    ('V', 'Vol'),
    ('E', 'Ecostand'),
)

TYPERADIATORKNOP_CHS = (
    ('G', 'Gewoon'),
    ('T', 'Thermostaat'),
)

TYPEVERLICHTING_CHS = (
    ('G', 'Gloeilamp'),
    ('T', 'TL'),
    ('H', 'Halogeen'),
    ('L', 'Led'),
)

TYPERAAMBEKLEDING_CHS = (
    ('G', 'Gordijn'),
    ('J', 'Jaloezie'),
    ('V', 'Vouwgordijnen'),
    ('R', 'Rolgordijnen'),
)

TYPETHERMOSTAAT_CHS = (
    ('G', 'Gewoon'),
    ('S', 'Met dag nacht stand'),
)

AANMELDWOONCORP_CHS = (
    ('V', 'Verhuizing'),
    ('P', 'Plaatsing nieuwe apparatuur'),
    ('K', 'Na een klacht'),
    ('Ko', 'Kleinschalig onderhoud'),
    ('Go', 'Grootschalig onderhoud'),
    ('On', 'Oplevering nieuwbouw'),
)

AANMELDZELF_CHS = (
    ('W', 'Website'),
    ('S', 'Social media'),
    ('M', 'Mailing'),
    ('B', 'Bewonersavond'),
    ('Wa', 'Wijkactie'),
    ('Vc', 'Verwijzing consulent'),
    ('Vb', 'Verwijzing mede-huurders'),
)

ADDRESS_CHOICES = (
    ('W', 'Woonadres'),
    ('B', 'Bezoekadres'),
    ('A', 'Afleveradres'),
    ('V', 'Verblijfadres'),
)

ACTIESTATUS_CHS = (
    ('O', 'Open'),
    ('U', 'In Uitvoering'),
    ('V', 'Volbracht'),
)


CNTHOEDANIGHEID_CHS = (
    ('W', 'Bedrijf'),
    ('H', 'Deskundige'),
)

MEDIUM_CHS = (
    ('M', 'Mobiel nummer'),
    ('H', 'Huistelefoon'),
    ('E', 'E-Mail'),
    ('F', 'Fax'),
    ('A', 'Facebook'),
    ('L', 'LinkedIn'),
    ('T', 'Twitter'),
)

GROEP_CHS = (
    ('B', 'Bedrijf'),
    ('I', 'Instantie'),
    ('S', 'Stichting'),
    ('O', 'Organisatie'),
    ('G', 'Gemeente'),
    ('R', 'Rijksoverheid'),
    ('A', 'Afdeling'),
)

TYPEWONING_CHS = (
    ('T', 'Tussenwoning'),
    ('H', 'Hoekwoning'),
    ('2', '2-1 Kap'),
    ('V', 'Vrijstaand'),
    ('A', 'Appartement'),
)

BOUWJAAR_CHS = (
    ('V', 'Voor 1980'),
    ('T', '1980 - 2000'),
    ('N', 'Na 2000'),
)

BEWONING_CHS = (
    ('H', 'Verhuur'),
    ('V', 'VVE'),
    ('E', 'Eigendom'),
)

TYPEVRAAG_CHS = (
    ('I', 'Info'),
    ('A', 'Advies'),
    ('O', 'Offerte'),
)


TYPEACTIVITEIT_CHS = (
    ('L', 'Lezing'),
    ('E', 'Excursie'),
    ('T', 'Thema-avond'),
    ('E', 'Project'),
    ('E', 'Excursie'),
)

ONDERWERPVRAAG_CHS = (
    ('Ea', 'Energie algemeen'),
    ('Eiv', 'Energie isolatie vloer'),
    ('Eim', 'Energie isolatie muur'),
    ('Eig', 'Energie isolatie glas'),
    ('Eid', 'Energie isolatie dak'),
    ('Ev', 'Energie verwarming'),
    ('Eo', 'Energie opwekking'),
    ('C', 'Circulair'),
    ('G', 'Groen'),
    ('O', 'Overig'),
)

STATUSVRAAG_CHS = (
    ('B', 'Beantwoord'),
    ('O', 'Onbeantwoord'),
    ('U', 'Wordt uitgezocht'),
)

BEOORDELING_CHS = (
    ('Z', 'Zeer Goed'),
    ('G', 'Goed'),
    ('V', 'Voldoende'),
    ('S', 'Slecht'),
    ('E', 'Zeer Slecht'),
)

def CheckForNone(theStr):
    if theStr is None:
        return ''
    else:
        return theStr + ' '

class Groep(models.Model):
    grp_GroupNm = models.CharField('Groep', max_length=45)
    grp_Website = models.CharField('Website', help_text='Plak hier de url van website', max_length=240, blank=True, null=True)
    grp_Notities = models.TextField('Notities', blank=True, null=True)
    grp_Type = models.CharField('Type groep', max_length=1, choices=GROEP_CHS, blank=True, null=True, default='O')

    def __str__(self):
        return CheckForNone(self.grp_GroupNm)

    class Meta:
        verbose_name_plural = 'Organisaties, Instanties, Bedrijven, enz.'
        verbose_name = 'Groep'


# Acties die ondernomen moeten worden aangaande contact
class Actie(models.Model):
    aci_Naam = models.CharField('Naam', max_length=85)
    aci_Omschr = models.TextField('Omschrijving', blank=True, null=True)
    aci_Status = models.CharField('Status', max_length=1, choices=ACTIESTATUS_CHS, blank=True, null=True, default='O')

    def __str__(self):
        return self.aci_Naam

    class Meta:
        verbose_name_plural = 'Acties'
        #verbose_name = 'Activiteit, Project, Lezing, enz.'


class Activiteit(models.Model):
    act_Naam = models.CharField('Naam / Titel', max_length=85, help_text='Naam van de activiteit, project of themadag')
    act_Omschr = models.TextField('Omschrijving', blank=True, null=True)
    act_Type = models.CharField('Type activiteit', max_length=1, choices=TYPEACTIVITEIT_CHS, blank=True, null=True, default='L')

    class Meta:
        verbose_name_plural = 'Activiteiten'
        verbose_name = 'Activiteit, Project, Lezing, enz.'

    def __str__(self):
        return self.act_Naam


# class TelfAdres(models.Model):
#     tad_Straat = models.CharField('Straat', max_length=100, blank=True, null=True)
#     tad_HuisNr = models.CharField('Huisnummer', max_length=10, blank=True, null=True)
#     tad_HuisNrToev = models.CharField('Toevoeging', max_length=10, blank=True, null=True)
#     #adr_Land = CountryField(multiple=False)
#     tad_PostCd = models.CharField('Postcode', max_length=15, blank=True, null=True)
#     tad_Plaats = models.CharField('Plaats', max_length=85, blank=True, null=True)
#     tad_Type = models.CharField('Type adres', max_length=1, choices=ADDRESS_CHOICES, blank=True, null=True, default='W')


class Contact(models.Model):
    cnt_Groepen = models.ManyToManyField(Groep, blank=True, verbose_name='Groep(en)', help_text='Groepen waaronder dit contact valt; ')
    cnt_Acties = models.ManyToManyField(Actie, blank=True, verbose_name='Acties', help_text='Acties (open) te nemen mbt dit contact; ', related_query_name='acties_related')
    cnt_VoorNm = models.CharField('Voornaam', max_length=45)
    cnt_AchterNm = models.CharField('Achternaam', max_length=65)
    cnt_TussenVgsl = models.CharField('Tussenvoegsel', max_length=15, blank=True, null=True)
    cnt_VoorLtrs = models.CharField('Voorletters', max_length=10, blank=True, null=True)
    cnt_Notities = models.TextField('Notities', blank=True, null=True)
    cnt_Type = models.CharField('Type contact', max_length=1, choices=CNTHOEDANIGHEID_CHS, blank=True, null=True, default='W')

    def __str__(self):
        return CheckForNone(self.cnt_VoorNm) + CheckForNone(self.cnt_TussenVgsl) + CheckForNone(self.cnt_AchterNm)

    class Meta:
        verbose_name_plural = 'Contacten'
        ordering = ("cnt_AchterNm", "cnt_VoorNm")




# Heeft ForeignKey in Vraag
class AdviesContact(Contact):
    cnt_Vastlegger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_query_name='Genoteerd door', verbose_name='Vastlegger')
    cnt_DatVastlegging = models.DateTimeField('Tijdstip van notatie', blank=True, null=True)
    cnt_Activiteit = models.ManyToManyField(Activiteit, blank=True, verbose_name='Activiteiten', help_text='Activiteiten waaraan dit contact deelneemt; ')
    cnt_NieuwsBrief = models.BooleanField('Nieuwbrief', blank=True, null=True, default=False, help_text='Dit aanvinken als het contact de nieuwsbrief wil ontvangen')

    def CheckOnbeAntw(self):
        for vraag in self.vraag_set.all():
            if vraag.vrg_StatusVraag == 'O':
                return 'Vraag open'
        return '- - -'

    def CheckCoachGespr(self):
        if self.coachgesprek_set == None:
            return False
        else:
            return True

    def __str__(self):
        return CheckForNone(self.cnt_VoorNm) + CheckForNone(self.cnt_TussenVgsl) + CheckForNone(self.cnt_AchterNm)

    class Meta:
        verbose_name_plural = 'Advies contacten'
        ordering = ("cnt_AchterNm", "cnt_VoorNm")

    def get_absolute_url(self):
        return reverse('drzData:upd_adviescontact', kwargs={'pk': self.id})

    CheckOnbeAntw.short_description = 'Vragen'


class Exposant(Groep):
    exp_Verhaal = models.TextField('Verhaal',
                                   help_text='Pitch, aandachtspunten, enz bij exposant zelf (Producten hebben apart verhaal)',
                                   blank=True, null=True)

    def __str__(self):
        return self.grp_GroupNm

    class Meta:
        verbose_name_plural = 'Exposanten'


class Woninggegevens(models.Model):
    Contact = models.ForeignKey(AdviesContact, on_delete=models.CASCADE, blank=True, null=True)
    wng_TypeWoning = models.CharField('Type Woning', max_length=1, choices=TYPEWONING_CHS, blank=True, null=True)
    wng_Bouwjaar = models.CharField('Bouwjaar', max_length=1, choices=BOUWJAAR_CHS, blank=True, null=True)
    wng_Bewoning = models.CharField('Type bewoning', max_length=1, choices=BEWONING_CHS, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Woninggegevens'

    def __str__(self):
        return CheckForNone(str(self.Contact)) + ' / ' + CheckForNone(self.get_wng_TypeWoning_display())




class Vraag(models.Model):
    Contact = models.ForeignKey(AdviesContact, on_delete=models.CASCADE, blank=True, null=True)
    vrg_TypeVraag = models.CharField('Type vraag', max_length=1, choices=TYPEVRAAG_CHS, blank=True, null=True)
    vrg_OnderwerpVraag = models.CharField('Onderwerp vraag', max_length=3, choices=ONDERWERPVRAAG_CHS, blank=True, null=True)
    vrg_StatusVraag = models.CharField('Status vraag', max_length=1, choices=STATUSVRAAG_CHS, blank=True, null=True)
    vrg_Tekst = models.TextField('Tekst vraag', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Vragen'

    def __str__(self):
        #return self.get_vrg_OnderwerpVraag_display() + ' / ' + self.vrg_Tekst[:14] + '...'
        #return CheckForNone(self.vrg_Tekst[:14]) + '...'
        return self.vrg_Tekst[:14] + '...'



class Adres(models.Model):
    Contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)
    Groep = models.ForeignKey(Groep, on_delete=models.CASCADE, blank=True, null=True)
    adr_Straat = models.CharField('Straat', max_length=100, blank=True, null=True)
    adr_HuisNr = models.CharField('Huisnummer', max_length=10, blank=True, null=True)
    adr_HuisNrToev = models.CharField('Toevoeging', max_length=10, blank=True, null=True)
    #adr_Land = CountryField(multiple=False)
    adr_PostCd = models.CharField('Postcode', max_length=15, blank=True, null=True)
    adr_Plaats = models.CharField('Plaats', max_length=85, blank=True, null=True)
    adr_type = models.CharField('Type adres', max_length=1, choices=ADDRESS_CHOICES, blank=True, null=True, default='W')
    adr_Notities = models.TextField('Notities', blank=True, null=True)

    def __str__(self):
        return CheckForNone(self.adr_Straat) + CheckForNone(self.adr_HuisNr) + CheckForNone(self.adr_Plaats)

    class Meta:
        verbose_name_plural = 'Adressen'


class Nummer(models.Model):
    Contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)
    Groep = models.ForeignKey(Groep, on_delete=models.CASCADE, blank=True, null=True)
    nmb_Number = models.CharField('Nummer', max_length=85, help_text='Mobiel, Telefoon, E-mail, Facebook, enz.')
    nmb_Medium = models.CharField('Medium', max_length=1, choices=MEDIUM_CHS, blank=True, null=True)
    nmb_Notities = models.CharField('Notitie', max_length=120, blank=True, null=True)

    def __str__(self):
        return self.nmb_Number


class Bezoekreden(models.Model):
    bzr_Naam = models.CharField('Reden', max_length=120)
    bzr_Omschr = models.TextField('Omschrijving', blank=True, null=True)

    def __str__(self):
        return self.bzr_Naam

    class Meta:
        verbose_name_plural = 'Bezoekredenen'


class WinkelBezoek(models.Model):
    AdviesContact = models.ForeignKey(AdviesContact, on_delete=models.CASCADE, blank=True, null=True)
    wbz_TijdStip = models.DateTimeField('Tijdstip van bezoek', blank=True, null=True)  #, auto_now_add=True
    wbz_Bezoeken = models.ManyToManyField(Bezoekreden, blank=True, verbose_name='Bezoekreden(en)')
    wbz_Notities = models.TextField('Notities', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Winkelbezoeken'
        ordering = ("wbz_TijdStip",)

    def __str__(self):
        return self.wbz_TijdStip.strftime("%Y-%m-%d %H:%M:%S")  #+ ' / ' + self.wbz_Bezoeken


class Product(models.Model):
    Exposant = models.ForeignKey(Exposant, on_delete=models.CASCADE, blank=True, null=True)
    prd_Naam = models.CharField('Product', max_length=85)


class Review(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    rvw_Tekst = models.TextField('Reviewtekst')
    rvw_Beoordeling = models.CharField('Medium', max_length=1, choices=BEOORDELING_CHS, blank=True, null=True)


class CoachGesprek(models.Model):
    cgs_AdviesContact = models.OneToOneField(AdviesContact, on_delete=models.CASCADE, blank=True, null=True, help_text='Kies bijbehorende adviescontact', verbose_name='Adviescontact')
    cgs_AanmeldingWoonCorp = models.CharField('Aanmeldingsrede Wooncooperatie', max_length=2, choices=AANMELDWOONCORP_CHS, blank=True, null=True, help_text='De reden van aanmelding indien aangemeld via wooncooperatie')
    cgs_AanmeldingZelf = models.CharField('Zelf aangemeld', max_length=2, choices=AANMELDZELF_CHS, blank=True, null=True, help_text='De reden van aanmelding indien zelf aangemeld')
    cgs_AanmeldAnders = models.TextField('Anders', blank=True, null=True, help_text='Vermeld hier andere reden voor aanmelding')
    cgs_IsModemAanw = models.BooleanField('Is er modem aanwezig in huis', blank=True, null=True)
    cgs_TypeCentrVent = models.CharField('Type centrale ventilatie', max_length=2, choices=TYPECENTRALEVENT_CHS, blank=True, null=True)
    cgs_TypeElektraMeter = models.CharField('Energiemeter', help_text='Wat voor energiemeter heeft geconstateerd?', choices=ENERGIEMETER_CHS, max_length=1, blank=True, null=True)
    # Telefonische voorbereiding
    cgs_HuurderInfo = models.TextField('Info huurder', help_text='Wat is er al bekend over de huurder', blank=True, null=True)
    cgs_DatTijdGesprek = models.DateTimeField('Datum en tijd gesprek', help_text='Datum en tijd dat het coachgesprek is ingeplanned', blank=True, null=True)
    cgs_WieAanWezig = models.TextField('Wie gaan aanwezig zijn', help_text='Wie gaan er tijdens het coach gesprek aanwezig zijn', blank=True, null=True)
    cgs_IsWoningToerAangekond = models.BooleanField('Woningtoer aangekondigd', help_text='Is aan de bewonders doorgegeven dat er een Woningtoer is?', blank=True, null=True)
    cgs_EnergieRekBijDeHand = models.BooleanField('Energierekening bij de hand', help_text='Heeft de bewoner de energierekening bij de hand voor tijdens het gesprek?', blank=True, null=True)
    cgs_ElektraMeter = models.CharField('Energiemeter', help_text='Wat voor energiemeter heeft de bewoner?', choices=ENERGIEMETER_CHS, max_length=1, blank=True, null=True)
    cgs_Motivatie = models.CharField('Motivatie', help_text='Wat is de motivatie voor de aanvraag?', choices=MOTIVATIE_CHS, max_length=2, blank=True, null=True)
    cgs_MotivatieAnders = models.TextField('Andere motivatie', help_text='Andere motivatie dan bovenstaand', blank=True, null=True)
    # Afsraakbevestiging
    cgs_IsDatumTijdBevestigd = models.BooleanField('Datum / Tijd bevestiging', help_text='Is de datum en tijd voor het coachgesprek bevestigd door de bewoner?', blank=True, null=True)
    cgs_IsDocsKlaarGelegd = models.BooleanField('Documenten klaargelegd', help_text='Zijn de documenten klaargelegd door de coach?', blank=True, null=True)
    cgs_IsWonToerHerAangeKond = models.BooleanField('Woningtoer heraangekondigd', help_text='Is aan de bewonders voor een twede keer doorgegeven dat er een Woningtoer is?', blank=True, null=True)
    cgs_IsInAgendGeplaatst = models.BooleanField('Coachgesprek in agenda coach', help_text='Heeft de coach het gesprek in zijn agenda geplaats?', blank=True, null=True)
    # Voorbereiding met de woningcorporatie (als mogelijk)
    cgs_GenomenEnergMaatr = models.TextField('Genomen energie maatregelen', help_text='Zijn er al energiemaatregelen genomen door de woningbouw?', blank=True, null=True)
    cgs_GeplandeEnrgMaatr = models.TextField('Geplande energie maatregelen', help_text='Heeft de woningbouw energiemaatregelen geplanned voor deze woning?', blank=True, null=True)
    cgs_EnergieLabel = models.TextField('Energielabel', help_text='Wat is het energielabel voor deze woning nu en straks?', blank=True, null=True)
    cgs_BekendeProbl = models.TextField('Bekende problemen', help_text='Zijn er bekende problemen aan deze woning (vocht, geluid)', blank=True, null=True)
    # Bespreken van wensen
    cgs_RedenEnergBesp = models.TextField('Reden van energiebesparen', help_text='Wat maakt dat u energie wilt besparen?', blank=True, null=True)
    cgs_RedenEnergBespAnderen = models.TextField('Reden van energiebesparen volgens anderen', help_text='Wat vinden de anderen (bewoners) over reden dat uw energie wilt besparen?', blank=True, null=True)
    cgs_ToekomstPlanWoning = models.TextField('Toekomstplannen voor de woning', help_text='Wat zijn de toekomstplannen die u heeft voor de woning, indien u die heeft?', blank=True, null=True)
    cgs_MetWieHierWonen = models.TextField('Met wie woont u hier', help_text='Met wie woont u in dit huis (medebewoners)?', blank=True, null=True)
    cgs_BudgetKlMaatr = models.TextField('Is er budget voor kleine besparingen', help_text='Is er budget voor kleine besparingen (om advies op af te stemmen)?', blank=True, null=True)
    cgs_IetsGedaanEnrgMaatr = models.TextField('Al iets gedaan aan energiebesparing', help_text='Heeft u al iets gedaan aanenergiebesparing? Wat?', blank=True, null=True)
    cgs_AfwijkEnergRek = models.TextField('Afwijking energierekening', help_text='wijkt de energierekening af van het gemiddelde? Is het (te) hoog?', blank=True, null=True)
    # Woningtoer
    # Algemeen
    cgs_TypeThermostaat = models.CharField('Type thermostaat', help_text='?', choices=TYPETHERMOSTAAT_CHS, max_length=1, blank=True, null=True)
    cgs_TypeRadiatorknop = models.CharField('Type radiatorknop', help_text='Type radiatorknoppen aanwezig in huis?', choices=TYPERADIATORKNOP_CHS, max_length=1, blank=True, null=True)
    cgs_TypeThermostaat = models.CharField('Type thermostaat', choices=TYPETHERMOSTAAT_CHS, max_length=1, blank=True, null=True)
    cgs_IsAquariumAanw = models.BooleanField('Is er een aquarium aanwezig', help_text='Is er in huis een aquarium aanwezig (ergens in huis)?', blank=True, null=True)
    cgs_IsAircoAanw = models.BooleanField('Is er Airco', help_text='Is er airco aanwezig in huis?', blank=True, null=True)
    # Woonkamer
    cgs_TypeRaambekleding_Wk = models.CharField('Type raambekleding', help_text='Type raambekleding in de woonkamer?', choices=TYPERAAMBEKLEDING_CHS, max_length=1, blank=True, null=True)
    cgs_TypeVerlichting_Wk = models.CharField('Type verlichting', help_text='Wat voor type verlichting is er aanwezig in de woonkamer?', choices=TYPEVERLICHTING_CHS, max_length=1, blank=True, null=True)
    cgs_Problemen_Wk = models.CharField('Problemen woonkamer', help_text='Constateerd u problemen in de woonkamer?', choices=TYPEPROBLEEM_CHS, max_length=1, blank=True, null=True)
    cgs_OverigOpmerk_Wk = models.TextField('Overige opmerkingen woonkamer', blank=True, null=True)
    #Keuken
    cgs_TypeWasMachGebruik = models.CharField('Type wasmachinegebruik', choices=TYPEWASMACHINEGEBRUIK_CHS, max_length=1, blank=True, null=True)
    cgs_IsKokenMetDeksel = models.BooleanField('Deksel op pan tijdens koken?', blank=True, null=True)
    cgs_TypeKookSysteem = models.CharField('Wijze van koken', help_text='Hoe kookt men, welke middelen gebruikt men daarvoor?', choices=TYPEKOOKSYSTEEM_CHS, max_length=1, blank=True, null=True)
    cgs_IsAfzuigingVrij = models.BooleanField('Is afzuiging vrij en schoon?', blank=True, null=True)
    cgs_IsCloseInBoilerAanw = models.BooleanField('Close in boiler aanwezig?', blank=True, null=True)
    cgs_AanwApperatuur = models.CharField('Aanwezige apparatuur', help_text='Overige aanwezige apperatuur', choices=KEUKENAPPARATUUR_CHS, max_length=2, blank=True, null=True)
    cgs_Problemen_K = models.CharField('Problemen keuken', help_text='Constateerd u problemen in de keuken?', choices=TYPEPROBLEEM_CHS, max_length=1, blank=True, null=True)
    cgs_OverigOpmerk_K = models.TextField('Overige opmerkingen keuken', blank=True, null=True)
    # Gang
    cgs_IsRadiatorAanw_Gng = models.BooleanField('Radiator aanwezig in gang?', blank=True, null=True)
    cgs_IsBrievenBusAanw_Gng = models.BooleanField('Brievenbus aanwezig in gang?', blank=True, null=True)
    cgs_TypeVerlichting_Gng = models.CharField('Type verlichting in gang', help_text='Wat voor type verlichting is er aanwezig in de Gang?', choices=TYPEVERLICHTING_CHS, max_length=1, blank=True, null=True)
    cgs_TypeTochtVoorziening_Gng = models.CharField('Type tochtvoorziening gang', choices=TYPETOCHTVOORZIENING_CHS, max_length=2, blank=True, null=True)
    cgs_Problemen_Gng = models.CharField('Problemen gang', help_text='Constateerd u problemen in de gang?', choices=TYPEPROBLEEM_CHS, max_length=1, blank=True, null=True)
    cgs_OverigOpmerk_Gng = models.TextField('Overige opmerkingen gang', blank=True, null=True)
    # CV ketel
    cgs_CVOnderhoud =  models.CharField('Type onderhoud cv ketel', help_text='Welke type onderhoud wordt er gepleegd aan de cb ketel?', choices=TYPECVKETELONDERHOUD_CHS, max_length=1, blank=True, null=True)
    cgs_CVTemperatuur = models.IntegerField('Temperatuur cv ketel', help_text='Op wat voor water temperatuur staat de CV ketel ingestel', blank=True, null=True)
    # Slaapkamer
    cgs_TypeVerlichting_Slk = models.CharField('Type verlichting slaapkamer', choices=TYPEVERLICHTING_CHS, max_length=1, blank=True, null=True)
    cgs_IsApparatuurStndBy = models.BooleanField('Apparatuur op standby aanwezig slaapkamer?', blank=True, null=True)
    cgs_IsVerwarmd = models.BooleanField('Word verwarming gebruikt in slaapkamer?', blank=True, null=True)
    cgs_IsAircoAanw_Slk = models.BooleanField('Is er Airco in slaapkamer', blank=True, null=True)
    cgs_TypeBed =  models.CharField('Type bedverwarming', choices=TYPEBEDVERWARMING_CHS, max_length=1, blank=True, null=True)
    cgs_Problemen_Slk = models.CharField('Problemen slaapkamer', help_text='Constateerd u problemen in de slaapkamer?', choices=TYPEPROBLEEM_CHS, max_length=1, blank=True, null=True)
    cgs_OverigOpmerk_Slk = models.TextField('Overige opmerkingen slaapkamer(s)', blank=True, null=True)
    # Tuin
    cgs_IsTuinVerlAanw = models.BooleanField('Is er tuinverlichting aanwezig?', blank=True, null=True)
    cgs_IsVijverpompAanw = models.BooleanField('Is er vijverpomp aanwezig?', blank=True, null=True)
    cgs_IsTerrasVerwAanw = models.BooleanField('Is er terrasverwarming?', blank=True, null=True)
    cgs_OverigOpmerk_Tn = models.TextField('Overige opmerkingen tuin', blank=True, null=True)
    # Schuur
    cgs_IsTwedeeKoelkAanw = models.BooleanField('Is er tweede koelkast aanwezig?', help_text='Of vrieskist', blank=True, null=True)
    cgs_OverigOpmerk_Sch = models.TextField('Overige opmerkingen schuur', blank=True, null=True)
    # Het advies
    cgs_BespaarAdviesTekst = models.TextField('Bespaar advies', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Coachgesprekken'

    def get_absolute_url(self):
        return reverse('drzData:upd_coachgesprek', kwargs={'pk': self.id})

    def __str__(self):
        return 'Gesprek: ' + str(self.cgs_AdviesContact)  #+ ' / ' + self.wbz_Bezoeken


class FollowUp(models.Model):
    Fup_AdviesContact = models.OneToOneField(AdviesContact, on_delete=models.CASCADE, blank=True, null=True)
    Fup_WelkeMaatrGenomen = models.TextField('Welke maatregelen zijn er genomen?', blank=True, null=True)
    Fup_WelkGedragVeranderd = models.TextField('Welke gedrag is er veranderd?', blank=True, null=True)
    Fup_WelkeVerderStappen = models.TextField('Welke verdere stappen kunnen er genomen worden?', blank=True, null=True)





