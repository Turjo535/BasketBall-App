from rest_framework import serializers
from .models import Player, Scouting_Context,Report_Model


class Player_Information_Serializers(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Player
        fields = ['user',
            'jersey',
            'height',
            'position',
            'class_year',
            'game_context',
            'gender',
            'opponent',
            'performance_note',]


class Report_Serializers(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model=Report_Model
        fields=[
            'user',
            'overview',
            'strength',
            'weaknesses', 
            'projection',
            'points_per_game', 
            'field_goal_percentage',
            'rebounds',
            'assists',
            'steals_and_blocks',]
        