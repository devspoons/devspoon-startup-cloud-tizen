from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Users
        fields = ('id','name','email','password','image','level','register_date')
