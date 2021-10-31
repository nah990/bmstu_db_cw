# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from django.conf.urls import url
from app import views


urlpatterns = [
    path('', views.index, name='home'),  # The home page
    # Matches any html file
    re_path(r'clear/', views.clear_selected_tickets, name='clear_selected_tickets'),
    re_path(r'tickets/', views.select_ticket, name='select_ticket'),
    re_path(r'addticket\.html$', views.ticket_add, name='add_ticket'),
    re_path(r'^.*\.html', views.pages, name='pages'),

]
