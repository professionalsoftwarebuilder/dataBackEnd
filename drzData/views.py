from datetime import datetime, time
from django.contrib import messages
from constance.admin import config
from django.views import View
from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, FormView, DetailView
from model_utils.models import now

from .models import WinkelBezoek
from .forms import WinkelBezoekForm, AdviesContactFrontForm, VraagInlineFormset, \
    WoninggegevensInlineFormset, CoachgesprekForm, AdviesContactListForm, \
    AdresInlineFormset, NummerInlineFormset, KlantSelfServFrontForm

from .models import *
from django.shortcuts import redirect
from django.urls import reverse

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.mail import EmailMessage
from datetime import datetime

from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    context = {}
    return render(request, 'drzData/index.html', context)

def contact(request):
    return render(request, 'drzData/contact.html', {})

def snd_bevestcoachgespr(request, pk):
    #print('In functie')
    #if request == 'GET':
    #print('In functie')
    # Eig moet eerst data worden opgeslagen (in geval er data is gewijzigd)
    # Bijbehoorende Adviescontact ophalen
    Gesprek = CoachGesprek.objects.get(id=pk)
    #Contact = AdviesContact.object.get(id=Gesprek.adviescontact.id)
    Contact = Gesprek.cgs_AdviesContact
    Bericht = config.BEVESTIGINGSMAIL_COACHGESPR_BODY.format(Contact.__str__, Gesprek.cgs_DatTijdGesprek)
    print('bericht opgemaakt')
    Nummers = Contact.nummer_set.all()
    ToEmail = None
    for nummer in Nummers:
        if nummer.nmb_Medium == 'E':
            ToEmail = nummer.nmb_Number

    if ToEmail is None:
        return render(request, 'drzData/add_coachgesprek.html', {'Warning': 'Het e-mail adres van het adviescontact ontbreek (mail niet verzonden)'})

    # Send the e-mail
    #Email_Adr =
    send_mail(
        'Bevestiging afpraak met Energiecoach Duurzaam Woorden', # Subject
        Bericht, # Message
        'energiecoach@duurzaamwoerden.nl', # From email
        ['vlietjames@gmail.com'], # To email
    )
    # If success update multiselect
    # Go back to page
    return render(request, 'drzData/add_coachgesprek.html', {'Warning': 'Het bevestigins e-mail is met succes verzonden' })



def prnt_lst_advcont(request, tag):
    # Create byte stream buffer
    buf = io.BytesIO()
    # Create a canvas
    canv = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textObj = canv.beginText()
    textObj.setTextOrigin(inch, inch)
    textObj.setFont('Courier', 14)
    contacten = None

    if tag == 'alAdvCnt':
        contacten = AdviesContact.objects.all()

    if tag == 'AdvCntOpnVrg':
        contacten = AdviesContact.objects.filter(vraag__vrg_StatusVraag='O')

    if tag == 'AdvCntCchGsp':
        contacten = AdviesContact.objects.exclude(coachgesprek=None)

    # Add some lines of text
    lines = []

    for contact in contacten:
        lines.append(contact.__str__())
        #lines.append(contact.cnt_Notities)
        if contact.nummer_set:
            for nummer in contact.nummer_set.all():
                lines.append(nummer.nmb_Number)
        lines.append('- - - - - - - -')

    for line in lines:
        textObj.textLine(line)

    canv.drawText(textObj)
    canv.showPage()
    canv.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='lst_cont.pdf')



class savewnkbzandnwcont(View):
    form_class = WinkelBezoekForm
    #initial = {'key': 'value'}
    template_name = 'drzData/add_winkelbezoek.html'




        #return render(request, self.template_name, {'form': form})


class add_winkelbezoek(CreateView):
    model = WinkelBezoek
    form_class = WinkelBezoekForm
    template_name = 'drzData/add_winkelbezoek.html'
    success_url = reverse_lazy('drzData:add_winkelbezoek')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            self.object = form.save()
            print('Winkelbezoek opgeslagen')
            if 'NieuwAdviesCont' in request.POST:
                return redirect(reverse("drzData:savewnkbzandnwcont", kwargs={'wnkbz': self.object.id}))
            else:
                return redirect(reverse("drzData:add_winkelbezoek"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_min = datetime.combine(datetime.today(), time.min)
        today_max = datetime.combine(datetime.today(), time.max)
        bezoeken = WinkelBezoek.objects.filter(wbz_TijdStip__range=(today_min, today_max))

        deLijst = []


        redenen = Bezoekreden.objects.all()
        count = redenen.count()
        for areden in redenen:
            deLijst.append([areden.bzr_Naam, 0])

        for bezoek in bezoeken:
            redenen = bezoek.wbz_Bezoeken.all()
            for reden in redenen:
                for i in range(count):
                    if reden.bzr_Naam == deLijst[i][0]:
                        deLijst[i][1] += 1

        extraContext = {'score': bezoeken.count(), 'redenen': deLijst}
        context.update(extraContext)
        return context


class add_adviescontact(CreateView):
    model = AdviesContact
    form_class = AdviesContactFrontForm
    template_name = 'drzData/add_adviescontact.html'
    #success_url = reverse_lazy('drzData:add_adviescontact')

    # def get_object(self, queryset=None):
    #     if 'pk' in self.kwargs:
    #         pk = self.kwargs['pk']
    #         obj = self.model.objects.get(id=pk)
    #     else:
    #         obj = None
    #
    #     return obj

    def get_context_data(self, **kwargs):
        context = super(add_adviescontact, self).get_context_data(**kwargs)
        extraContext = {'vraag_formset': VraagInlineFormset(),
                        'woninggeg_formset': WoninggegevensInlineFormset(),
                        'nummer_formset': NummerInlineFormset(),
                        'adres_formset': AdresInlineFormset(),
                        }
        context.update(extraContext)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     extraContext = {'score': bezoeken.count(), 'redenen': deLijst}
    #     context.update(extraContext)
    #     return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        vraag_formset = VraagInlineFormset(self.request.POST)
        woninggeg_formset = WoninggegevensInlineFormset(self.request.POST)
        nummer_formset = NummerInlineFormset(self.request.POST)
        adres_formset = AdresInlineFormset(self.request.POST)

        if vraag_formset.is_valid():
            print('vraag formset is valid')
        else:
            print('vraag formset is invalid')

        if adres_formset.is_valid():
            print('adres formset is valid')
        else:
            print('adres formset is invalid')

        #args = (vraag_formset, woninggeg_formset)
        #if form.is_valid() and vraag_formset.is_valid() and woninggeg_formset.is_valid():
        #if form.is_valid() and vraag_formset.is_valid():
        #if form.is_valid() and woninggeg_formset.is_valid():
        if form.is_valid() and woninggeg_formset.is_valid() and \
                    vraag_formset.is_valid() and nummer_formset.is_valid() and adres_formset.is_valid():
            return self.form_valid(form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset)
            #return self.form_valid(form)
        else:
            return self.form_invalid(form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset)

    def form_valid(self, form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset):
    #def form_valid(self, form):
        self.object = form.save(commit=False)
        #ctx = self.get_context_data()
        # Deze view kan ook vanuit winkelbezoek zijn aangeroepen!!!
        # In dat geval wordt hier de winkelbezoek gekoppeld
        if 'wnkbz' in self.kwargs:
            theId = self.kwargs.get('wnkbz')
            print('the id is: ' + str(theId))
            wnkbz = WinkelBezoek.objects.get(id=theId)
            #wnkbz.adviescontact = self.object
            #wnkbz.objects.save()
            self.object.save()
            self.object.winkelbezoek_set.add(wnkbz, bulk=False)
            print('winkelbezoek gekoppeld')
        else:
            self.object.save()
        form.save_m2m()

        # context = self.get_context_data()
        # vraag_formset = context['vraag_formset']
        # woninggeg_formset = context['woninggeg_formset']
        vragen = vraag_formset.save(commit=False)
        woninggeg = woninggeg_formset.save(commit=False)
        nummers = nummer_formset.save(commit=False)
        adressen = adres_formset.save(commit=False)

        for vraag in vragen:
            vraag.adviescontact = self.object
            self.object.vraag_set.add(vraag, bulk=False)

        for wgeg in woninggeg:
            wgeg.adviescontact = self.object
            self.object.woninggegevens_set.add(wgeg, bulk=False)

        for nummer in nummers:
            nummer.adviescontact = self.object
            self.object.nummer_set.add(nummer, bulk=False)

        for adres in adressen:
            adres.adviescontact = self.object
            self.object.adres_set.add(adres, bulk=False)

        return redirect(reverse("drzData:upd_adviescontact", kwargs={'pk': self.object.id}))


    def form_invalid(self, form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset):
        # context = self.get_context_data()
        # vraag_formset = context['vraag_formset']
        # woninggeg_formset = context['woninggeg_formset']
        return self.render_to_response(
            self.get_context_data(form=form,
                                  woninggeg_formset=woninggeg_formset,
                                  vraag_formset=vraag_formset))



class upd_adviescontact(UpdateView):
    model = AdviesContact
    form_class = AdviesContactFrontForm
    template_name = 'drzData/add_adviescontact.html'
    #success_url = reverse_lazy('drzData:add_adviescontact')

    # def get_object(self, queryset=None):
    #     if 'pk' in self.kwargs:
    #         pk = self.kwargs['pk']
    #         obj = self.model.objects.get(id=pk)
    #     else:
    #         obj = None
    #
    #     return obj

    def get_context_data(self, **kwargs):
        context = super(upd_adviescontact, self).get_context_data(**kwargs)

        extraContext = {
            'vraag_formset': VraagInlineFormset(instance=self.object),
            'woninggeg_formset': WoninggegevensInlineFormset(instance=self.object),
            'nummer_formset': NummerInlineFormset(instance=self.object),
            'adres_formset': AdresInlineFormset(instance=self.object),
        }

        context.update(extraContext)
        return context

    def post(self, request, *args, **kwargs):
        print('in post')
        # Get and prepare the form object
        pk = self.kwargs['pk']
        self.object = self.model.objects.get(id=pk)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance = self.object

        # Vraag tekst ophalen
        form_data = request.POST.dict()
        vraagtekst = form_data.get('vraagtekst', None)

        vraag_formset = VraagInlineFormset(self.request.POST, instance=self.object)
        woninggeg_formset = WoninggegevensInlineFormset(self.request.POST, instance=self.object)
        nummer_formset = NummerInlineFormset(self.request.POST, instance=self.object)
        adres_formset = AdresInlineFormset(self.request.POST, instance=self.object)




        if vraag_formset.is_valid():
            print('vraag formset is valid')
        else:
            print('vraag formset is invalid')
        #args = (vraag_formset, woninggeg_formset)
        #if form.is_valid() and vraag_formset.is_valid() and woninggeg_formset.is_valid():
        #if form.is_valid() and vraag_formset.is_valid():
        if form.is_valid() and woninggeg_formset.is_valid() and \
                vraag_formset.is_valid() and nummer_formset.is_valid() and adres_formset.is_valid():
            print('Form is valid')
            return self.form_valid(form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset)
            #return self.form_valid(form)
        else:
            return self.form_invalid(form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset)

    def form_valid(self, form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset):
    #def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        #form.save_m2m()

        vragen = vraag_formset.save()
        woninggeg = woninggeg_formset.save()
        nummers = nummer_formset.save()
        adressen = adres_formset.save()

        print('bericht opgemaakt')




    # for vraag in vragen:
        #     vraag.adviescontact = self.object
        #     self.object.vraag_set.add(vraag, bulk=False)
        #
        # for wgeg in woninggeg:
        #     wgeg.adviescontact = self.object
        #     self.object.woninggegevens_set.add(wgeg, bulk=False)

        # dikt = {'vraag_formset': vragen, 'woninggeg_formset': woninggeg}
        # self.get_context_data(dikt)

                # Go back to page

        return redirect(reverse("drzData:upd_adviescontact", kwargs={'pk': self.object.id}))

    def form_invalid(self, form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset):
        # context = self.get_context_data()
        # vraag_formset = context['vraag_formset']
        # woninggeg_formset = context['woninggeg_formset']
        return self.render_to_response(
            self.get_context_data(form=form,
                                    vraag_formset=vraag_formset,
                                    woninggeg_formset=woninggeg_formset,
                                  ))


class dtl_adviescontact(DetailView):
    model = AdviesContact
    paginate_by = 35
    context_object_name = 'AdviesContact'
    form_class = AdviesContactListForm
    template_name = 'drzData/lst_adviescontact.html'




class lst_adviescontact(ListView):
    model = AdviesContact
    paginate_by = 25
    context_object_name = 'AdviesContact'
    form_class = AdviesContactListForm
    template_name = 'drzData/lst_adviescontact.html'
    success_url = reverse_lazy('drzData:lst_adviescontact')

    def get_context_data(self, **kwargs):
        context = super(lst_adviescontact, self).get_context_data(**kwargs)

        extraContext = {'theTitle': 'Alle adviescontacten',
                        'ShowCoachGsprLink': 'False',
                        'Tag': 'alAdvCnt'}
        context.update(extraContext)
        return context


class lst_advcont_opnvraag(ListView):
    model = AdviesContact
    paginate_by = 35
    context_object_name = 'AdviesContact'
    queryset = AdviesContact.objects.filter(vraag__vrg_StatusVraag='O')
    form_class = AdviesContactListForm
    template_name = 'drzData/lst_adviescontact.html'
    success_url = reverse_lazy('drzData:lst_adviescontact')

    def get_context_data(self, **kwargs):
        context = super(lst_advcont_opnvraag, self).get_context_data(**kwargs)

        extraContext = {'theTitle': 'Adviescontacten met open vragen',
                        'ShowCoachGsprLink': 'False',
                        'Tag': 'AdvCntOpnVrg'}
        context.update(extraContext)
        return context


class lst_advcont_coachgespr(ListView):
    model = AdviesContact
    paginate_by = 35
    context_object_name = 'AdviesContact'
    queryset = AdviesContact.objects.exclude(coachgesprek=None)
    form_class = AdviesContactListForm
    template_name = 'drzData/lst_adviescontact.html'
    success_url = reverse_lazy('drzData:lst_adviescontact')

    def get_context_data(self, **kwargs):
        context = super(lst_advcont_coachgespr, self).get_context_data(**kwargs)

        extraContext = {'theTitle': 'Adviescontacten met coachgesprekken',
                        'ShowCoachGsprLink': 'True',
                        'Tag': 'AdvCntCchGsp'}
        context.update(extraContext)
        return context


class add_coachgesprek(CreateView):
    model = CoachGesprek
    form_class = CoachgesprekForm
    template_name = 'drzData/add_coachgesprek.html'
    #success_url = reverse_lazy('drzData:upd_coachgesprek')

    # def get_success_url(self):
    #     self.success_url = reverse_lazy('drzData:upd_coachgesprek', kwargs={'pk': self.object.id})
    #     return self.success_url

theVar = ''

class upd_coachgesprek(UpdateView):
    model = CoachGesprek
    form_class = CoachgesprekForm
    template_name = 'drzData/add_coachgesprek.html'
    CtrlField = 'Hallo'

    def get_context_data(self, **kwargs):
        context = super(upd_coachgesprek, self).get_context_data(**kwargs)
        global theVar
        #context['CtrlField'] = self.CtrlField
        #context['CtrlField'] = self.request.POST.get('theTab')
        context['CtrlField'] = theVar
        #print(context)
        return context


    def post(self, request, *args, **kwargs):
        print('in post')
        global theVar
        # Get and prepare the form object
        pk = self.kwargs['pk']
        # if 'Ctrl' in kwargs:
        #     self.CtrlField = kwargs.get('Ctrl')

        theTab = request.POST.get('theTab')
        if theTab:
            #self.CtrlField = theTab
            theVar = theTab

        print(self.CtrlField)

        self.object = self.model.objects.get(id=pk)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance = self.object

        if form.is_valid():
            print('Form is valid')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()

        # Als sendbevestigingsmail geklikt was
        if 'sendmail' in self.request.POST:
            print('mail verzenden')
            SndSuc = True
            Gesprek = self.object
            Contact = Gesprek.cgs_AdviesContact
            CoachNm = Contact.cnt_Vastlegger.first_name
            BccMail = Contact.cnt_Vastlegger.email
            print(BccMail)
            if Gesprek.cgs_DatTijdGesprek:
                DatumGspr = Gesprek.cgs_DatTijdGesprek.strftime("%d-%m-%Y, %H:%M")
                Bericht = config.BEVESTIGINGSMAIL_COACHGESPR_BODY.format(Contact, DatumGspr, CoachNm)
                print('bericht opgemaakt')
                Onderwerp = 'Afspraakbevestiging bezoek energiecoach duurzaamwoerden op: ' + DatumGspr


                Nummers = Contact.nummer_set.all()
                ToEmail = None

                for nummer in Nummers:
                    if nummer.nmb_Medium == 'E':
                        ToEmail = nummer.nmb_Number

                if ToEmail is None:
                    print('Ontbrekend email adres')
                    messages.success(self.request, f'Het e-mail adres van het adviescontact ontbreek (mail niet verzonden)')
                    SndSuc = False




            else:
                SndSuc = False
                messages.success(self.request, f'Datum en/of tijd van de afspraak ontbreekt (mail niet verzonden)')


            if SndSuc:
                try:
                    email = EmailMessage(
                        Onderwerp,  # Subject
                        Bericht,  # Message
                        'energiecoach@duurzaamwoerden.nl',  # From email
                        [ToEmail],  # To email
                        [BccMail, 'energiecoach@duurzaamwoerden.nl']
                    )
                    email.send(fail_silently=False)
                except:
                    SndSuc = False
                    messages.success(self.request, f'Er ging iets fout tijdens het verzenden van de bevestigingsmail')

            if SndSuc:
                print('met success verzonden')
                messages.success(self.request, f'Het bevestigins e-mail is met succes verzonden')

                # If success update multiselect
                Statussen = Gesprek.cgs_StatusGesprek
                print(Statussen)
                if not 'E' in Statussen:
                    Statussen.append('E')
                    Gesprek.cgs_StatusGesprek
                    Gesprek.save()

                # Go back to page

        return redirect(reverse("drzData:upd_coachgesprek", kwargs={'pk': self.object.id}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


def mail_vraag(request, vrg_id, cnt_id):
    deVraag = Vraag.objects.get(id=vrg_id)
    print('mail verzenden')
    SndSuc = True
    # De adviescontact
    Contact = deVraag.Contact
    # De Afhandelaars
    Afhandelaars = deVraag.vrg_Afhandelaren.all()
    # Haal mail adressen op
    BccMails = []
    for afhnd in Afhandelaars:
        BccMails.append(afhnd.email)

    BccMail = config.BCC_MAILADRESS_BEVESTIGINGSMAIL_ADVIESCONTACTVRAAG
    BccMails.append(BccMail)
    print(BccMails)
    # Tijdstip dat vraag gesteld is, is niet bekend eigenlijk, hoeft niet zelfde te zijn als tijdstip registratie adviescontact
    #currentdate = datetime.now()
    #DatumVrg = currentdate.strftime("%d-%m-%Y, %H:%M")  #deVraag.cgs_DatTijdGesprek.strftime("%d-%m-%Y, %H:%M")
    DatumVrg = deVraag.vrg_DatVastlegging
    Bericht = config.BEVESTIGINGSMAIL_ADVIESCONTACTVRAAG_BODY.format(Contact, DatumVrg, deVraag.vrg_Tekst)
    print('bericht opgemaakt')
    Onderwerp = 'Terugkoppeling op uw vraag aan Duurzaam Woerden op: ' + DatumVrg.strftime("%m-%d-%Y %H:%M:%S")

    Nummers = Contact.nummer_set.all()
    ToEmail = None

    for nummer in Nummers:
        if nummer.nmb_Medium == 'E':
            ToEmail = nummer.nmb_Number

    if ToEmail is None:
        print('Ontbrekend email adres')
        messages.success(request, f'Het e-mail adres van het adviescontact ontbreek (mail niet verzonden)')
        SndSuc = False

    if SndSuc:
        try:
            email = EmailMessage(
                Onderwerp,  # Subject
                Bericht,  # Message
                BccMail,  # From email
                [ToEmail],  # To email
                BccMails
            )
            email.send(fail_silently=False)
        except:
            SndSuc = False
            messages.success(request, f'Er ging iets fout tijdens het verzenden van de bevestigingsmail naar Adviescontact: ' + str(Contact))

    if SndSuc:
        print('met success verzonden')
        messages.success(request, f'Het bevestigins e-mail is met succes verzonden')

        # If success update status vraag naar in behandeling
        deVraag.vrg_StatusVraag = 'U'
        deVraag.save()

    return redirect(reverse("drzData:upd_adviescontact", kwargs={'pk': cnt_id}))


#---------------------------------------


class add_klantselfserv(CreateView):
    model = AdviesContact
    form_class = KlantSelfServFrontForm
    template_name = 'drzData/add_klantselfserv.html'
    #success_url = reverse_lazy('drzData:add_adviescontact')

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            VraagTekst = form.cleaned_data['cnt_VraagTekst']
            print(VraagTekst)


        if form.is_valid():
            return self.form_valid(form, VraagTekst)
            #return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, VraagTekst):
    #def form_valid(self, form):
        self.object = form.save(commit=False)
        # Deze view kan ook vanuit winkelbezoek zijn aangeroepen!!!
        # In dat geval wordt hier de winkelbezoek gekoppeld
        if 'wnkbz' in self.kwargs:
            theId = self.kwargs.get('wnkbz')
            print('the id is: ' + str(theId))
            wnkbz = WinkelBezoek.objects.get(id=theId)
            #self.object.save()
            self.object.winkelbezoek_set.add(wnkbz, bulk=False)
            print('winkelbezoek gekoppeld')
        # else:
        #     self.object.save()

        #self.object.save()
        # Vraag aanmaken en toevoegen
        DeVraag = Vraag(vrg_Tekst=VraagTekst, vrg_StatusVraag='O', Contact=self.object)

        # Vastlegger op user duurzaam zetten
        VastLegger = User.objects.get(username='duurzaam')

        self.object.cnt_Vastlegger = VastLegger
        self.object.save()
        print('Vastlegger duurzaam gesaved')

        DeVraag.save()

        form.save_m2m()

        return redirect(reverse("drzData:add_klantselfserv"))


    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


# Let op: class hieronder wordt niet gebruikt
class upd_klantselfserv(UpdateView):
    model = AdviesContact
    form_class = KlantSelfServFrontForm
    template_name = 'drzData/add_klantselfserv.html'
    #success_url = reverse_lazy('drzData:add_adviescontact')

    # def get_object(self, queryset=None):
    #     if 'pk' in self.kwargs:
    #         pk = self.kwargs['pk']
    #         obj = self.model.objects.get(id=pk)
    #     else:
    #         obj = None
    #
    #     return obj

    def get_context_data(self, **kwargs):
        context = super(upd_klantselfserv, self).get_context_data(**kwargs)

        extraContext = {
            'vraag_formset': VraagInlineFormset(instance=self.object),
            'woninggeg_formset': WoninggegevensInlineFormset(instance=self.object),
            'nummer_formset': NummerInlineFormset(instance=self.object),
            'adres_formset': AdresInlineFormset(instance=self.object),

        }

        context.update(extraContext)
        return context

    def post(self, request, *args, **kwargs):
        print('in post')
        # Get and prepare the form object
        pk = self.kwargs['pk']
        self.object = self.model.objects.get(id=pk)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance = self.object

        # Vraag tekst ophalen
        form_data = request.POST.dict()
        vraagtekst = form_data.get('vraagtekst', None)

        vraag_formset = VraagInlineFormset(self.request.POST, instance=self.object)
        woninggeg_formset = WoninggegevensInlineFormset(self.request.POST, instance=self.object)
        nummer_formset = NummerInlineFormset(self.request.POST, instance=self.object)
        adres_formset = AdresInlineFormset(self.request.POST, instance=self.object)




        if vraag_formset.is_valid():
            print('vraag formset is valid')
        else:
            print('vraag formset is invalid')

        if form.is_valid():
            VraagTekst = form.cleaned_data['cnt_VraagTekst']
            print(VraagTekst)


        #args = (vraag_formset, woninggeg_formset)
        #if form.is_valid() and vraag_formset.is_valid() and woninggeg_formset.is_valid():
        #if form.is_valid() and vraag_formset.is_valid():
        if form.is_valid() and woninggeg_formset.is_valid() and \
                vraag_formset.is_valid() and nummer_formset.is_valid() and adres_formset.is_valid():
            print('Form is valid')
            return self.form_valid(form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset, VraagTekst)
            #return self.form_valid(form)
        else:
            return self.form_invalid(form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset)

    def form_valid(self, form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset, VraagTekst):
    #def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        #form.save_m2m()

        # Vraagrecord ophalen, moet de eerste zijn
        DeVraag = self.object.vraag_set[0]
        DeVraag.vrg_Tekst = VraagTekst
        DeVraag.save()

        vragen = vraag_formset.save()
        woninggeg = woninggeg_formset.save()
        nummers = nummer_formset.save()
        adressen = adres_formset.save()

        print('bericht opgemaakt')




    # for vraag in vragen:
        #     vraag.adviescontact = self.object
        #     self.object.vraag_set.add(vraag, bulk=False)
        #
        # for wgeg in woninggeg:
        #     wgeg.adviescontact = self.object
        #     self.object.woninggegevens_set.add(wgeg, bulk=False)

        # dikt = {'vraag_formset': vragen, 'woninggeg_formset': woninggeg}
        # self.get_context_data(dikt)

                # Go back to page

        return redirect(reverse("drzData:upd_klantselfserv", kwargs={'pk': self.object.id}))

    def form_invalid(self, form, vraag_formset, woninggeg_formset, nummer_formset, adres_formset):
        # context = self.get_context_data()
        # vraag_formset = context['vraag_formset']
        # woninggeg_formset = context['woninggeg_formset']
        return self.render_to_response(
            self.get_context_data(form=form,
                                    vraag_formset=vraag_formset,
                                    woninggeg_formset=woninggeg_formset,
                                  ))


def in_aanbouw(request):
    context = {}
    return render(request, 'drzData/in_aanbouw.html', context)