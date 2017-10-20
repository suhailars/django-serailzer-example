# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from invoice.models import Invoice, Transaction

# Register your models here.
class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1
    show_change_link = True
    classes = ['collapse']

class InvoiceAdmin(admin.ModelAdmin):
    inlines = (TransactionInline, )


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Transaction)
