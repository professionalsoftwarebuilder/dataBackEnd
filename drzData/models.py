from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

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
    ('W', 'Winkelklant'),
    ('H', 'Huisbezoek'),
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

def CheckForNone(theStr):
    if theStr is None:
        return ''
    else:
        return theStr + ' '


class Groep(models.Model):
    grp_GroupNm = models.CharField('Groep', max_length=45)
    grp_Website = models.CharField('Website', help_text='Plak hier de url van website van groep', max_length=240, blank=True, null=True)
    grp_Notities = models.TextField('Notities', blank=True, null=True)
    grp_Type = models.CharField('Type groep', max_length=1, choices=GROEP_CHS, blank=True, null=True, default='O')

    def __str__(self):
        return CheckForNone(self.grp_GroupNm)

    class Meta:
        verbose_name_plural = 'Organisaties, Instanties, Bedrijven, enz.'
        verbose_name = 'Groep'


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

class Contact(models.Model):
    cnt_Vastlegger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_query_name='Genoteerd door', verbose_name='Vastlegger')
    cnt_DatVastlegging = models.DateTimeField('Tijdstip van notatie', blank=True, null=True)
    cnt_Groepen = models.ManyToManyField(Groep, blank=True, verbose_name='Groep(en)', help_text='Groepen waaronder dit contact valt; ')
    cnt_Acties = models.ManyToManyField(Actie, blank=True, verbose_name='Acties', help_text='Acties (open) mbt dit contact; ', related_query_name='acties_related')
    cnt_Activiteit = models.ManyToManyField(Activiteit, blank=True, verbose_name='Activiteiten', help_text='Activiteiten waaraan dit contact deelneemt; ')
    cnt_VoorNm = models.CharField('Voornaam', max_length=45)
    cnt_AchterNm = models.CharField('Achternaam', max_length=65)
    cnt_TussenVgsl = models.CharField('Tussenvoegsel', max_length=15, blank=True, null=True)
    cnt_VoorLtrs = models.CharField('Voorletters', max_length=10, blank=True, null=True)
    cnt_Notities = models.TextField('Notities', blank=True, null=True)
    cnt_Type = models.CharField('Type contact', max_length=1, choices=CNTHOEDANIGHEID_CHS, blank=True, null=True, default='W')
    cnt_NieuwsBrief = models.BooleanField('Nieuwbrief', blank=True, null=True, default=False, help_text='Dit aanvinken als het contact de nieuwsbrief wil ontvangen')

    def CheckOnbeAntw(self):
        for vraag in self.vraag_set.all():
            if vraag.vrg_StatusVraag == 'O':
                return 'Vraag open'
        return '- - -'


    def __str__(self):
        return CheckForNone(self.cnt_VoorNm) + CheckForNone(self.cnt_TussenVgsl) + CheckForNone(self.cnt_AchterNm)

    class Meta:
        verbose_name_plural = 'Contacten'
        ordering = ("cnt_AchterNm", "cnt_VoorNm")

    CheckOnbeAntw.short_description = 'Vragen'


class Adres(models.Model):
    Contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)
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


class AdresGroep(models.Model):
    Groep = models.ForeignKey(Groep, on_delete=models.CASCADE, blank=True, null=True)
    adg_Straat = models.CharField('Straat', max_length=100, blank=True, null=True)
    adg_HuisNr = models.CharField('Huisnummer', max_length=10, blank=True, null=True)
    adg_HuisNrToev = models.CharField('Toevoeging', max_length=10, blank=True, null=True)
    #adg_Land = CountryField(multiple=False)
    adg_PostCd = models.CharField('Postcode', max_length=15, blank=True, null=True)
    adg_Plaats = models.CharField('Plaats', max_length=85, blank=True, null=True)
    adg_type = models.CharField('Type adres', max_length=1, choices=ADDRESS_CHOICES, blank=True, null=True, default='W')
    adg_Notities = models.TextField('Notities', blank=True, null=True)

    def __str__(self):
        return CheckForNone(self.adg_Straat) + CheckForNone(self.adg_HuisNr) + CheckForNone(self.adg_Plaats)

    class Meta:
        verbose_name_plural = 'Adressen Groepen'


class NummerGroep(models.Model):
    Groep = models.ForeignKey(Groep, on_delete=models.CASCADE, blank=True, null=True)
    nmg_Number = models.CharField('Nummer', max_length=85, help_text='Mobiel, Telefoon, E-mail, Facebook, enz.')
    nmg_Medium = models.CharField('Medium', max_length=1, choices=MEDIUM_CHS, blank=True, null=True)
    nmg_Notities = models.CharField('Notitie', max_length=120, help_text='Kanttekening bij dit medium', blank=True, null=True)

    def __str__(self):
        return self.nmg_Number


class Woninggegevens(models.Model):
    Contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)
    wng_TypeWoning = models.CharField('Type Woning', max_length=1, choices=TYPEWONING_CHS, blank=True, null=True)
    wng_Bouwjaar = models.CharField('Bouwjaar', max_length=1, choices=BOUWJAAR_CHS, blank=True, null=True)
    wng_Bewoning = models.CharField('Type bewoning', max_length=1, choices=BEWONING_CHS, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Woninggegevens'

    def __str__(self):
        return str(self.Contact) + ' / ' + self.get_wng_TypeWoning_display()




class Vraag(models.Model):
    Contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)
    vrg_TypeVraag = models.CharField('Type vraag', max_length=1, choices=TYPEVRAAG_CHS, blank=True, null=True)
    vrg_OnderwerpVraag = models.CharField('Onderwerp vraag', max_length=3, choices=ONDERWERPVRAAG_CHS, blank=True, null=True)
    vrg_StatusVraag = models.CharField('Status vraag', max_length=1, choices=STATUSVRAAG_CHS, blank=True, null=True)
    vrg_Tekst = models.TextField('Tekst vraag', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Vragen'

    def __str__(self):
        return self.get_vrg_OnderwerpVraag_display() + ' / ' + self.vrg_Tekst[:14] + '...'


class Leverancier(models.Model):
    lvr_Naam = models.CharField('Naam', max_length=45, help_text='Naam Leverancier')
    lvr_Notities = models.TextField('Notities', blank=True, null=True)

    def __str__(self):
        return self.lvr_Naam

    class Meta:
        verbose_name_plural = 'Leveranciers'
        ordering = ("lvr_Naam",)


class Nummer(models.Model):
    Contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)
    Leverancier = models.ForeignKey(Leverancier, on_delete=models.CASCADE, blank=True, null=True)
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
    wbz_TijdStip = models.DateTimeField('Tijdstip van bezoek', blank=True, null=True)  #, auto_now_add=True
    wbz_Bezoeken = models.ManyToManyField(Bezoekreden, blank=True, verbose_name='Bezoekreden(en)')

    class Meta:
        verbose_name_plural = 'Winkelbezoeken'
        ordering = ("wbz_TijdStip",)

    def __str__(self):
        return self.wbz_TijdStip.strftime("%Y-%m-%d %H:%M:%S")  #+ ' / ' + self.wbz_Bezoeken