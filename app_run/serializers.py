from rest_framework import serializers
from .models import Run


class RunSerializer(serializers.ModelSerializer):
    model = Run
    fields = '__all__'