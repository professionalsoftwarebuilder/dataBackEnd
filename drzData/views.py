from datetime import datetime, time
from django.views import View
from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, FormView, DetailView
from .models import WinkelBezoek
from .forms import WinkelBezoekForm, AdviesContactFrontForm, VraagInlineFormset, \
    WoninggegevensInlineFormset, CoachgesprekForm, AdviesContactListForm

from .models import *
from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    context = {}
    return render(request, 'drzData/index.html', context)

def contact(request):
    return render(request, 'drzData/contact.html', {})


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

        for vraag in vragen:
            vraag.adviescontact = self.object
            self.object.vraag_set.add(vraag, bulk=False)

        for wgeg in woninggeg:
            wgeg.adviescontact = self.object
            self.object.woninggegevens_set.add(wgeg, bulk=False)

        print(str(self.object.id))

        return redirect(reverse("drzData:upd_adviescontact", kwargs={'pk': self.object.id}))

    def form_invalid(self, form, vraag_formset, woninggeg_formset):
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

        # extraContext = {'vraag_formset': VraagInlineFormset(kwargs['vraag_formset']),
        #                   'woninggeg_formset': WoninggegevensInlineFormset(kwargs['woninggeg_formset'])}
        extraContext = {'vraag_formset': VraagInlineFormset(instance = self.object),
                          'woninggeg_formset': WoninggegevensInlineFormset(instance=self.object)}
        #extraContext = kwargs

        context.update(extraContext)
        return context

    def post(self, request, *args, **kwargs):

        # Get and prepare the form object
        pk = self.kwargs['pk']
        self.object = self.model.objects.get(id=pk)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance = self.object

        vraag_formset = VraagInlineFormset(self.request.POST, instance=self.object)
        woninggeg_formset = WoninggegevensInlineFormset(self.request.POST, instance=self.object)
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
        self.object = form.save()
        self.object.save()
        #form.save_m2m()

        vragen = vraag_formset.save()
        woninggeg = woninggeg_formset.save()

        # for vraag in vragen:
        #     vraag.adviescontact = self.object
        #     self.object.vraag_set.add(vraag, bulk=False)
        #
        # for wgeg in woninggeg:
        #     wgeg.adviescontact = self.object
        #     self.object.woninggegevens_set.add(wgeg, bulk=False)

        # dikt = {'vraag_formset': vragen, 'woninggeg_formset': woninggeg}
        # self.get_context_data(dikt)

        return redirect(reverse("drzData:upd_adviescontact", kwargs={'pk': self.object.id}))

    def form_invalid(self, form, vraag_formset, woninggeg_formset):
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
    paginate_by = 35
    context_object_name = 'AdviesContact'
    form_class = AdviesContactListForm
    template_name = 'drzData/lst_adviescontact.html'
    success_url = reverse_lazy('drzData:lst_adviescontact')

    def get_context_data(self, **kwargs):
        context = super(lst_adviescontact, self).get_context_data(**kwargs)

        extraContext = {'theTitle': 'Alle adviescontacten',
                        'ShowCoachGsprLink': 'False'}
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
                        'ShowCoachGsprLink': 'False'}
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
                        'ShowCoachGsprLink': 'True'}
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


class upd_coachgesprek(UpdateView):
    model = CoachGesprek
    form_class = CoachgesprekForm
    template_name = 'drzData/add_coachgesprek.html'
    # #success_url = reverse_lazy('drzData:upd_coachgesprek')
    #
    # def get_success_url(self):
    #     self.success_url = reverse_lazy('drzData:upd_coachgesprek', kwargs={'pk': self.object.id})
    #     return self.success_url