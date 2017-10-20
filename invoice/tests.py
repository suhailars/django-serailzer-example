# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from invoice.models import Invoice, Transaction


connection = APIClient()
class InvoiceTests(APITestCase):
    def setUp(self):
        self.post_data = {
            "customer": "test",
            "transactions": [
                {
                    "product": "test prod",
                    "quantity": 4,
                    "price": "10.00"
                },
                {
                    "product": "prod",
                    "quantity": 4,
                    "price": "10.00"      
                }
            ]
        }

    def test_create_invoice_success(self):        
        response = connection.post('/invoices/', self.post_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.post_data.pop("transactions")
        response = connection.post('/invoices/', self.post_data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_create_invoice_fail(self):        
        self.post_data.pop("transactions")
        response = connection.post('/invoices/', self.post_data, format='json')
        self.assertEqual(response.status_code, 400)

                
    def test_update_invoice_success_with_transaction_id(self):
        response = connection.post('/invoices/', self.post_data, format='json')          
        id_ = str(response.data["id"])
        response = connection.get('/invoices/' + id_ + "/" , format='json')
        update_data = response.data
        total_quantity = update_data["total_quantity"]
        total_amount = float(update_data["total_amount"])
        update_data["transactions"][0]["quantity"] = 5
        response = connection.put('/invoices/' + id_ + "/" , update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(total_quantity + 1, response.data["total_quantity"])

    def test_update_invoice_success_with_new_transaction(self):
        product_test = {
            "product": "prod",
            "quantity": 4,
            "price": "10.00"      
        }
        response = connection.post('/invoices/', self.post_data, format='json')          
        id_ = str(response.data["id"])
        response = connection.get('/invoices/' + id_ + "/" , format='json')
        update_data = response.data
        total_amount = float(update_data["total_amount"])
        update_data["transactions"].append(product_test)
        total_amount += 4 * 10.0
        response = connection.put('/invoices/' + id_ + "/" , update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(total_amount, float(response.data["total_amount"]))

    def test_update_invoice_success_with_missing_transaction(self):
        response = connection.post('/invoices/', self.post_data, format='json')          
        id_ = str(response.data["id"])
        response = connection.get('/invoices/' + id_ + "/" , format='json')
        update_data = response.data
        transactions = update_data["transactions"]
        transaction_to_delete = transactions.pop()
        amount_deleted = float(transaction_to_delete["line_total"])
        total_amount = float(update_data["total_amount"])
        response = connection.put('/invoices/' + id_ + "/" , update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(float(response.data["total_amount"]), total_amount - amount_deleted)

    def test_update_invoice_fail_with_id_not_exist(self):
        id_ = "1"
        response = connection.put('/invoices/' + id_ + "/" , self.post_data, format='json')
        self.assertEqual(response.status_code, 404)
 

