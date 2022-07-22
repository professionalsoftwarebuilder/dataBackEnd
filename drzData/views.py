from datetime import datetime, time

from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import WinkelBezoek
from .forms import WinkelBezoekForm, AdviesContactFrontForm, VraagInlineFormset, \
    WoninggegevensInlineFormset, CoachgesprekForm

from .models import *
from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    context = {}
    return render(request, 'drzData/index.html', context)

def contact(request):
    return render(request, 'drzData/contact.html', {})

class add_winkelbezoek(CreateView):
    model = WinkelBezoek
    form_class = WinkelBezoekForm
    template_name = 'drzData/add_winkelbezoek.html'
    success_url = reverse_lazy('drzData:add_winkelbezoek')

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
    success_url = reverse_lazy('drzData:add_adviescontact')

    def get_context_data(self, **kwargs):
        context = super(add_adviescontact, self).get_context_data(**kwargs)
        extraContext = {'vraag_formset': VraagInlineFormset(),
                        'woninggeg_formset': WoninggegevensInlineFormset()}
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
        if vraag_formset.is_valid():
            print('vraag formset is valid')
        else:
            print('vraag formset is invalid')
        #args = (vraag_formset, woninggeg_formset)
        #if form.is_valid() and vraag_formset.is_valid() and woninggeg_formset.is_valid():
        #if form.is_valid() and vraag_formset.is_valid():
        if form.is_valid() and woninggeg_formset.is_valid():
            return self.form_valid(form, vraag_formset, woninggeg_formset)
            #return self.form_valid(form)
        else:
            return self.form_invalid(form, vraag_formset, woninggeg_formset)

    def form_valid(self, form, vraag_formset, woninggeg_formset):
    #def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()

        # context = self.get_context_data()
        # vraag_formset = context['vraag_formset']
        # woninggeg_formset = context['woninggeg_formset']
        vragen = vraag_formset.save(commit=False)
        woninggeg = woninggeg_formset.save(commit=False)

        for vraag in vragen:
            vraag.adviescontact = self.object
            self.object.vraag_set.add(vraag, bulk=False)

        for wgeg in woninggeg:
            wgeg.adviescontact = self.object
            self.object.woninggegevens_set.add(wgeg, bulk=False)

        return redirect(reverse("drzData:add_adviescontact"))

    def form_invalid(self, form, vraag_formset, woninggeg_formset):
        # context = self.get_context_data()
        # vraag_formset = context['vraag_formset']
        # woninggeg_formset = context['woninggeg_formset']
        return self.render_to_response(
            self.get_context_data(form=form,
                                  woninggeg_formset=woninggeg_formset,
                                  vraag_formset=vraag_formset))

class add_coachgesprek(CreateView):
    model = CoachGesprek
    form_class = CoachgesprekForm
    template_name = 'drzData/add_coachgesprek.html'
    success_url = reverse_lazy('drzData:add_coachgesprek')
