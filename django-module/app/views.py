# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from datetime import datetime

from psycopg2.sql import NULL

from app.utils import set_pagination
from django.contrib.auth.models import User
from orders.models import Order, StockInfo
from .forms import AddTicketForm
from .site_fetcher import gov_capital, get_name_by_ticket, leo_prophet


def user_role_check(user):
    return user.groups.filter(name='specialist').exists() or user.groups.filter(name='admin').exists()


def specialist_role_check(user):
    return user.groups.filter(name='specialist').exists()


def user_role(user):
    if user.groups.filter(name='specialist').exists():
        return "Specialist"
    if user.groups.filter(name='admin').exists():
        return "Admin"
    return "User"


array_of_id = []


@login_required(login_url="/login/")
def index(request):
    global array_of_id
    context = {'segment': 'index'}
    html_template = loader.get_template('dashboard.html')
    context['today_date'] = datetime.date(datetime.now())
    context['total_users'] = User.objects.all().count()
    context['current_role'] = user_role(request.user)
    context['user_role_check'] = user_role_check(request.user)
    context['total_tickets'] = StockInfo.objects.all().count()
    context['tickets'], context['info'] = set_pagination(request, StockInfo.objects.all().order_by('-id'), item_numer=8)
    orders_month_report, orders_month_report_labels = Order.orders_month_report()
    orders_month_report = orders_month_report.filter(ticket_id__in=array_of_id)
    context['orders_month_report'] = list(orders_month_report)
    context['orders_month_report_labels'] = orders_month_report_labels
    context['orders'], context['info'] = set_pagination(request,
                                                        Order.objects.filter(ticket_id__in=array_of_id).order_by('-id'),
                                                        item_numer=10)
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def select_ticket(request):
    context = {'segment': 'index'}
    global array_of_id
    array_of_id.append(request.path.split('/')[-1])
    return redirect("/", context)


@login_required(login_url="/login/")
def clear_selected_tickets(request):
    context = {'segment': 'index'}
    global array_of_id
    array_of_id = []
    return redirect("/", context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def ticket_add(request):
    if not request.user.is_superuser:
        context = {}
        html_template = loader.get_template('page-403.html')
        return HttpResponse(html_template.render(context, request))
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if form.is_valid():
            print("Adding ticket: " + request.POST['addTicketField'])
            ticket = request.POST['addTicketField']
            name = get_name_by_ticket(ticket)
            data = gov_capital(ticket)
            stock_info = StockInfo.objects.create(name=name, ticket=ticket, source='Gov-Capital')
            stock_info.save()
            ticket_id = stock_info.id
            i = 0
            while i < len(data):
                Order.objects.create(ticket_id=StockInfo.objects.get(pk=ticket_id), created_time=data[i],
                                     price=data[i + 1], min_price=data[i + 2], max_price=data[i + 3],
                                     updated_time=data[i], product_name=ticket)
                i = i + 4

            print("Leo Prophet start")
            data = leo_prophet(ticket)
            stock_info = StockInfo.objects.create(name=name, ticket=ticket, source='Leo-Prophet')
            stock_info.save()
            ticket_id = stock_info.id
            i = 0
            while i < len(data):
                Order.objects.create(ticket_id=StockInfo.objects.get(pk=ticket_id), created_time=data[i],
                                     price=data[i + 1], min_price=data[i + 2], max_price=data[i + 3],
                                     updated_time=data[i], product_name=ticket)
                i = i + 4

    form = AddTicketForm()

    return render(request, 'addticket.html', {'form': form})
