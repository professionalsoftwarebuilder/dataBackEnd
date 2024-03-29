from django.urls import path
from . import views
from django.contrib import admin

app_name = 'drzData'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('add_winkelbezoek/', views.add_winkelbezoek.as_view(), name='add_winkelbezoek'),
    path('add_coachgesprek/', views.add_coachgesprek.as_view(), name='add_coachgesprek'),
    path('upd_coachgesprek/<int:pk>', views.upd_coachgesprek.as_view(), name='upd_coachgesprek'),
    path('add_adviescontact/', views.add_adviescontact.as_view(), name='add_adviescontact'),
    path('upd_adviescontact/<int:pk>', views.upd_adviescontact.as_view(), name='upd_adviescontact'),
    path('lst_adviescontact/', views.lst_adviescontact.as_view(), name='lst_adviescontact'),
    path('lst_advcont_opnvraag/', views.lst_advcont_opnvraag.as_view(), name='lst_advcont_opnvraag'),
    path('lst_advcont_coachgespr/', views.lst_advcont_coachgespr.as_view(), name='lst_advcont_coachgespr'),

    # Klant "selfservice scherm"
    path('add_klantselfserv/', views.add_klantselfserv.as_view(), name='add_klantselfserv'),
    path('upd_klantselfserv/<int:pk>', views.upd_klantselfserv.as_view(), name='upd_klantselfserv'),

    path('savewnkbzandnwcont/<int:wnkbz>', views.add_adviescontact.as_view(), name='savewnkbzandnwcont'),
    path('prnt_lst_advcont/<str:tag>', views.prnt_lst_advcont, name='prnt_lst_advcont'),
    path('snd_bevestcoachgespr/<int:pk>', views.snd_bevestcoachgespr, name='snd_bevestcoachgespr'),
    path('mail_vraag/<int:vrg_id>/<int:cnt_id>', views.mail_vraag, name='mail_vraag'),

    path('in_aanbouw', views.in_aanbouw, name='in_aanbouw'),
]

admin.site.site_header = 'Duurzaam Woerden Gegevensbeheer'                    # default: "Django Administration"
admin.site.index_title = 'Overzicht Administratie'                 # default: "Site administration"
admin.site.site_title = 'DW administratie' # default: "Django site admin"
