# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Invoice(models.Model):
    customer = models.CharField(max_length=30)
    date = models.DateField(auto_now=True)
    total_quantity = models.IntegerField(default=0)
    total_amount = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    
    class Meta:
        db_table = 'invoices'

class Transaction(models.Model):

    product = models.CharField(max_length=30)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    line_total = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    invoice_id = models.ForeignKey(Invoice, related_name='transactions')
    
    class Meta:
        db_table = 'transactions'

