from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=250)
    fb_id = serializers.CharField(max_length=100)