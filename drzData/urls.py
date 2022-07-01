from django.urls import path
from . import views
from django.contrib import admin

app_name = 'drzData'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('add_winkelbezoek/', views.add_winkelbezoek.as_view(), name='add_winkelbezoek'),
]

admin.site.site_header = 'Duurzaam Woerden Gegevensbeheer'                    # default: "Django Administration"
admin.site.index_title = 'Overzicht Administratie'                 # default: "Site administration"
admin.site.site_title = 'DW administratie' # default: "Django site admin"
