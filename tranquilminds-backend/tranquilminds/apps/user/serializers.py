from rest_framework import serializers
from apps.user.models import *


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'  

