from urllib.parse import urlencode

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .forms import ContactForm, AdresForm, NummerForm, AdresGrForm, NummerGrForm
from .models import Groep, Contact, Adres, Nummer, NummerGroep, AdresGroep, Woninggegevens, Vraag, Activiteit, Leverancier, Actie, WinkelBezoek, Bezoekreden


class NummerInline(admin.StackedInline):
    model = Nummer
    exclude = ('Leverancier', )
    form = NummerForm
    extra = 0


class NummerInlineLev(admin.StackedInline):
    model = Nummer
    exclude = ('Contact', )
    form = NummerForm
    extra = 0


class AdresInline(admin.StackedInline):
    model = Adres
    form = AdresForm
    extra = 0


class NummerGroepInline(admin.StackedInline):
    model = NummerGroep
    form = NummerGrForm
    extra = 0


class AdresGroepInline(admin.StackedInline):
    model = AdresGroep
    form = AdresGrForm
    extra = 0


class TypeWoningInline(admin.StackedInline):
    model = Woninggegevens
    extra = 0


class VraagInline(admin.StackedInline):
    model = Vraag
    extra = 0


class LeverancierAdmin(admin.ModelAdmin):
    inlines = (NummerInlineLev,)


class GroepAdmin(admin.ModelAdmin):
    inlines = (AdresGroepInline, NummerGroepInline,)


class ContactAdmin(admin.ModelAdmin):
    inlines = (AdresInline, NummerInline, TypeWoningInline, VraagInline)
    form = ContactForm
    list_display = ('cnt_VoorNm', 'cnt_AchterNm', 'CheckOnbeAntw', 'view_acties_link', 'view_vragen_link', 'view_woongeg_link')


    def view_acties_link(self, obj):
        count = obj.cnt_Acties.count()
        url = (
                reverse("admin:drzData_actie_changelist")
                + "?"
                + urlencode({"acties__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Acties</a>', url, count)


    def view_vragen_link(self, obj):
        count = obj.vraag_set.count()
        url = (
            reverse("admin:drzData_vraag_changelist")
            + "?"
            + urlencode({"contact__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Vragen</a>', url, count)


    def view_woongeg_link(self, obj):
        count = obj.woninggegevens_set.count()
        url = (
            reverse("admin:drzData_woninggegevens_changelist")
            + "?"
            + urlencode({"woninggegevens__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Woninggegevens</a>', url, count)

    # specify a stylesheet just for the list view
    class Media:
        css = {'all': ('css/mymodel_list.css',)}

    view_vragen_link.short_description = "Vragen"
    view_woongeg_link.short_description = 'Woninggeg.'
    view_acties_link.short_description = 'Acties'


admin.site.register(Groep, GroepAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Vraag)
admin.site.register(Woninggegevens)
admin.site.register(Leverancier, LeverancierAdmin)
admin.site.register(Activiteit)
admin.site.register(Actie)
admin.site.register(Bezoekreden)
admin.site.register(WinkelBezoek)