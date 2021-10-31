# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin

from orders.models import Order, StockInfo


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ['id', 'product_name', 'price', 'created_time']


@admin.register(Order)
class OrderAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['product_name', 'price', 'created_time']
    search_fields = ['product_name']
    resource_class = OrderResource


@admin.register(StockInfo)
class StockInfo(admin.ModelAdmin):
    list_display = ('name', 'ticket', 'source')
    list_filter = ('id', 'name', 'ticket')
