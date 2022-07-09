from urllib.parse import urlencode

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .forms import ContactForm, AdresForm, NummerForm, ExposantForm, AdviesContactForm, VraagForm
from .models import Groep, Contact, Adres, Nummer, Woninggegevens, Vraag, Activiteit, Actie, WinkelBezoek, Bezoekreden, Exposant, AdviesContact


class NummerCntInline(admin.StackedInline):
    model = Nummer
    exclude = ('Groep',)
    form = NummerForm
    extra = 0


class NummerGrpInline(admin.StackedInline):
    model = Nummer
    exclude = ('Contact',)
    form = NummerForm
    extra = 0


class AdresCntInline(admin.StackedInline):
    model = Adres
    form = AdresForm
    exclude = ('Groep',)
    extra = 0


class AdresGrpInline(admin.StackedInline):
    model = Adres
    form = AdresForm
    exclude = ('Contact',)
    extra = 0


class TypeWoningInline(admin.StackedInline):
    model = Woninggegevens
    extra = 0


class VraagInline(admin.StackedInline):
    model = Vraag
    form = VraagForm
    extra = 0


class ExposantAdmin(admin.ModelAdmin):
    inlines = (NummerGrpInline, AdresGrpInline)
    form = ExposantForm


class GroepAdmin(admin.ModelAdmin):
    inlines = (AdresGrpInline, NummerGrpInline,)
    list_filter = ('exposant',)

    def get_queryset(self, request):
        qs = super(GroepAdmin, self).get_queryset(request)
        return qs.filter(exposant__isnull=True)


class ContactAdmin(admin.ModelAdmin):
    inlines = (NummerCntInline, AdresCntInline)
    form = ContactForm
    #filter_horizontal = ('cnt_Groepen',)
    list_display = ('cnt_VoorNm', 'cnt_AchterNm',)

    def get_queryset(self, request):
        qs = super(ContactAdmin, self).get_queryset(request)
        return qs.filter(adviescontact__isnull=True)


class AdviesContactAdmin(admin.ModelAdmin):
    inlines = (NummerCntInline, AdresCntInline, TypeWoningInline, VraagInline)
    form = AdviesContactForm
    exclude = ('cnt_Groepen',)
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
admin.site.register(Exposant, ExposantAdmin)
admin.site.register(Activiteit)
admin.site.register(Actie)
admin.site.register(Bezoekreden)
admin.site.register(WinkelBezoek)
admin.site.register(AdviesContact, AdviesContactAdmin)