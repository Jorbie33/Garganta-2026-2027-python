from django.contrib import admin

# Register your models here.
from  .models import User 

admin.site.register(user)

from rest_framework import serializers
from .models import user

class UseSerializer(Serializers.modelSerializer):
    class meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar']