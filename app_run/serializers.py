from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Run, AthleteInfo, Challenge, Position
from rest_framework import status


class RunUSerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']



class RunSerializer(serializers.ModelSerializer):
    athlete_data = RunUSerSerializer(read_only=True, source = "athlete", )
    class Meta:
        model = Run
        fields = '__all__'
    


class UserSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished',]

    def get_type(self,obj):
        if obj.is_staff:
            return "coach"
        else:
            return "athlete"
        
    def get_runs_finished(self,obj):
        return obj.run_set.filter(status = Run.Status.FINISHED).count()
    

class AthleteInfoSerialzer(serializers.ModelSerializer):
    class Meta:
        model = AthleteInfo
        fields = ('goals','weight', 'user_id' )
  
class ChallengesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('full_name', 'athlete')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('run', 'latitude', 'longitude', 'id')

    def validate_latitude(self, value):
        if -90 > value or value > 90 :
            raise serializers.ValidationError("Широта должна находиться в диапазоне от -90.0 до +90.0 градусов (включительно)")
        return value
    
    def validate_longitude(self, value):
        if value < -180 or value > 180 :
            raise serializers.ValidationError("долгота должна находиться в диапазоне от -180.0 до +180.0 градусов (включительно)")
        return value
    
    def validate_run(self, value):
        if value.status != Run.Status.IN_PROGRESS:
            raise serializers.ValidationError()
        return value
