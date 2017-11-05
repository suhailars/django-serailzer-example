import requests
import urllib
import json
from django.conf import settings
from account.models import AppUser, FBPages



class FbApi(object):

    def __init__(self):
        self.app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY
        self.app_secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET
        self.access_token = ""

    def get_long_lived_token(self, token):
        base_url = "https://graph.facebook.com/oauth/access_token"
        params = {'client_id': self.app_id, 'client_secret': self.app_secret, 'fb_exchange_token': token, 'grant_type': 'fb_exchange_token'}
        params_encode = urllib.urlencode(params)
        full_url = "%s?%s" % (base_url, params_encode)
        response = requests.get(full_url)
        if response.status_code == 200:
             text = json.loads(response.text)
             self.access_token = text.get("access_token", "")
        return self.access_token

    def get_user(self):
        base_url = "https://graph.facebook.com/v2.8/me"
        params = {
            'fields': "id,name,email",        
            'access_token': self.access_token
        }
        params_encode = urllib.urlencode(params)
        full_url = "%s?%s" % (base_url, params_encode)
        response = requests.get(full_url)
        if response.status_code == 200:
            text = json.loads(response.text)
            print "text", text
            return text

    def get_pages(self, user):
        if not self.access_token:
            user_db = AppUser.objects.get(user=user)
            self.access_token = user_db.access_token
        base_url = "https://graph.facebook.com/v2.8/me/accounts/"
        params = {'access_token': self.access_token}
        params_encode = urllib.urlencode(params)
        full_url = "%s?%s" % (base_url, params_encode)
        response = requests.get(full_url)
        print (response, dir(response))
        if response.status_code == 200:
            text = json.loads(response.text)
            print (text, type(text)) 
            pages = []
            try:
                for item in text["data"]:
                    print "items **************",item
                    page_id = item["id"]
                    name = item["name"]
                    category = item["category"]
                    page_token = item["access_token"]
                    pages.append({
                        "page_id": page_id,
                        "name": name,
                        "category": category
                    })
                    try:
                        page = FBPages.objects.get(page_id=page_id)
                    except:
                        FBPages.objects.create(name=name, page_id=page_id, user=user, category=category, access_token=page_token)
            except:
                print "accepted ********"
            return pages

    def get_pageinfo(self, page_id, fields="price_range,parking,hours", user=None):
        if not user and not self.access_token:
            return
        if not self.access_token:
            user_db = AppUser.objects.get(user=user)
            self.access_token = user_db.access_token

        if not page_id:
            return
        base_url = "https://graph.facebook.com/%s" % (page_id)
        params = {'access_token': self.access_token, "fields": fields}
        params_encode = urllib.urlencode(params)
        full_url = "%s?%s" % (base_url, params_encode)
        response = requests.get(full_url)
        print (response, dir(response))
        if response.status_code == 200:
            return response.json() 

    def update_pageinfo(self, page_id, data=None):
        user_db = ""
        try:
            user_db = FBPages.objects.get(page_id=page_id)
        except:
            user_db = user_db
        if not user_db:
            return
        access_token = user_db.access_token

        if not page_id or not data:
            return
        print "access_token ******"
        base_url = "https://graph.facebook.com/%s" % (page_id)
        params = {'access_token': access_token}
        params_encode = urllib.urlencode(params)
        full_url = "%s?%s" % (base_url, params_encode)
        response = requests.post(full_url, data=data)
        print (response, dir(response))
        print response.text
        if response.status_code == 200:
            return response.json() 
        







