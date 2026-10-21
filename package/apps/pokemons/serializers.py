from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    c_pass = serializers.CharField(write_only=True)
    
    class META:
        model = User
        fields = ['id', 'username', 'email', 'password', 
            'c_pass', ]
        
        def create(self, validated_data):
            c_pass = validated_data.pop("c_pass")
            password = validated_data.get("password")
            