from django.contrib import admin

from .forms import ContactForm, AdresForm, NummerForm, AdresGrForm, NummerGrForm
from .models import Groep, Contact, Adres, Nummer, NummerGroep, AdresGroep, Woninggegevens, Vraag


class NummerInline(admin.StackedInline):
    model = Nummer
    form = NummerForm
    extra = 1


class AdresInline(admin.StackedInline):
    model = Adres
    form = AdresForm
    extra = 1


class NummerGroepInline(admin.StackedInline):
    model = NummerGroep
    form = NummerGrForm
    extra = 1


class AdresGroepInline(admin.StackedInline):
    model = AdresGroep
    form = AdresGrForm
    extra = 1


class TypeWoningInline(admin.StackedInline):
    model = Woninggegevens
    extra = 0


class VraagInline(admin.StackedInline):
    model = Vraag
    extra = 0


class GroepAdmin(admin.ModelAdmin):
    inlines = (AdresGroepInline, NummerGroepInline )


class ContactAdmin(admin.ModelAdmin):
    inlines = (AdresInline, NummerInline, TypeWoningInline, VraagInline)
    form = ContactForm


admin.site.register(Groep, GroepAdmin)
admin.site.register(Contact, ContactAdmin)

