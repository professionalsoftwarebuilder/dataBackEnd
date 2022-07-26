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
    path('savewnkbzandnwcont/<int:wnkbz>', views.add_adviescontact.as_view(), name='savewnkbzandnwcont'),

]

admin.site.site_header = 'Duurzaam Woerden Gegevensbeheer'                    # default: "Django Administration"
admin.site.index_title = 'Overzicht Administratie'                 # default: "Site administration"
admin.site.site_title = 'DW administratie' # default: "Django site admin"
