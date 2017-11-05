# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import Http404
from .fb_api import FbApi
from django.contrib.auth import authenticate, login, logout
from account.models import AppUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


from .serializers import (
    AccountSerializer,
)

# from .models import ( 
#     Invoice,
#     Transaction,
# )


class LoginView(APIView):
    """
    Register a new user.
    """
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        print data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            #serializer.save()
            data = serializer.data
            fb_id = data["fb_id"]
            api = FbApi()
            token = api.get_long_lived_token(data["token"])
            user = authenticate(fb_id=fb_id)
            auth_token = None
            if user is not None:
                au = AppUser.objects.get(user=user)
                au.access_token = token
                au.save()
                auth_token = Token.objects.get(user=user)
            else:
                user_data = api.get_user()
                user = User.objects.create(username=user_data['name'], email=user_data['email'])
                AppUser.objects.create(user=user, fb_id=fb_id, access_token=token)
                user = authenticate(fb_id=fb_id)
                if user is not None:
                    auth_token = Token.objects.create(user=user)
                    print auth_token
            return Response({"auth_token": auth_token.key, "name": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        #invoices = Invoice.objects.alls()
        #serializer = InvoiceSerializer(invoices, many=True)
        return Response({})

class PageView(APIView):
    def get(self, request, format=None):
        user = request.user
        pages = []
        if user:
            api = FbApi()
            pages = api.get_pages(user)
            print pages

        #invoices = Invoice.objects.all()
        #serializer = InvoiceSerializer(invoices, many=True)
        return Response({"pages": pages})

class PageInfo(APIView):
    def get(self, request, pk, format=None):
        user = request.user
        page_id = pk
        pages = None
        if user and pk:
            api = FbApi()
            pages = api.get_pageinfo(page_id, user=user)
            print pages

        #invoices = Invoice.objects.all()
        #serializer = InvoiceSerializer(invoices, many=True)
        return Response({"pages": pages})

    def post(self, request, pk, format=None):
        user = request.user
        page_id = pk
        pages = None
        data = request.data
        print data
        if user and pk:
            api = FbApi()
            #pages = api.get_pageinfo(page_id, user=user)
            #print pages
            for key, val in data.items():
                if key != "price_range":
                    data[key] = json.dumps(val)

            print "data ******", data
            pages = api.update_pageinfo(page_id, data)


        #invoices = Invoice.objects.all()
        #serializer = InvoiceSerializer(invoices, many=True)
        return Response({"pages": pages})
