import json
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import Http404


from .serializers import (
    InvoiceSerializer,
    TransactionSerializer,
)

from .models import ( 
    Invoice,
    Transaction,
)


class InvoiceList(APIView):
    """
    Register a new user.
    """
    serializer_class = InvoiceSerializer
    #permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        print data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({"id":data["id"]}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)




class InvoiceDetails(APIView):

    serializer_class = InvoiceSerializer
    #permission_classes = (AllowAny,)
    
    def get_object(self, pk):
        try:
            return Invoice.objects.get(pk=pk)
        except Size.DoesNotExist:
            raise Http404    

    def get(self, request, pk, format=None):
        invoice = self.get_object(pk)
        serializer = self.serializer_class(invoice)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        invoice = self.get_object(pk)
        serializer = self.serializer_class(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        invoice = self.get_object(pk)
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)