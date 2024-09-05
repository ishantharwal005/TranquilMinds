from rest_framework import serializers
from apps.therapist.models import *


class therapistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapistModel
        fields = '__all__'  

