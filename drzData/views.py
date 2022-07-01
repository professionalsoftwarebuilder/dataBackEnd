from datetime import datetime, time

from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import WinkelBezoek
from .forms import WinkelBezoekForm

from .models import *

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
