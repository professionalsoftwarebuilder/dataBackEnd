from django.contrib import admin
from .models import Groep, Contact, Adres, Nummer, NummerGroep, AdresGroep, Woninggegevens, Vraag


class AdresInline(admin.TabularInline):
    model = Adres
    extra = 0


class NummerInline(admin.TabularInline):
    model = Nummer
    extra = 0


class NummerGroepInline(admin.TabularInline):
    model = NummerGroep
    extra = 0


class AdresGroepInline(admin.TabularInline):
    model = AdresGroep
    extra = 0


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


admin.site.register(Groep, GroepAdmin)
admin.site.register(Contact, ContactAdmin)

