from django.db import models
from UserAccount.models import User  

class Player(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player')  
    jersey = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    position = models.CharField(max_length=50)
    class_year = models.CharField(max_length=10)
    game_context = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    opponent = models.CharField(max_length=255)
    performance_note = models.TextField(blank=True, null=True)
    image=models.ImageField(blank=True, null=True)
    game_video=models.FileField(upload_to="video/%y",blank=True, null=True)

    def __str__(self):
        return f"{self.user.name} - Jersey {self.jersey}"
    
class Scouting_Context(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament_name=models.CharField(max_length=100)
    game_result=models.CharField(max_length=50)
    opponent_faced=models.CharField(max_length=50)
    score_or_margin=models.CharField(max_length=50)
    game_flow_details=models.TextField()

    def __str__(self):
        return f"{self.opponent_faced}"
    


class Report_Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    overview=models.TextField()
    strength = models.TextField()
    weaknesses = models.TextField()
    projection = models.TextField()
    points_per_game = models.DecimalField(max_digits=5, decimal_places=1)
    field_goal_percentage = models.DecimalField(max_digits=5, decimal_places=1)
    rebounds = models.DecimalField(max_digits=5, decimal_places=1)
    assists = models.DecimalField(max_digits=5, decimal_places=1)
    steals_and_blocks = models.DecimalField(max_digits=5, decimal_places=1)
    
    def __str__(self):
        return f"Report for {self.user.name}"