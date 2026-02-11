from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Run, AthleteInfo, Challenge


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