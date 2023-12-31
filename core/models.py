from django.db import models

class Player(models.Model):
    img_url = models.TextField(blank=True)
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=10)
    age = models.IntegerField(default=0)
    team = models.CharField(max_length=50)
    league = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    date_game = models.DateTimeField(default=None)
    opponent = models.CharField(max_length=50)
    games_played = models.IntegerField(default=0)
    games_started = models.IntegerField(default=0)
    minutes_played = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    field_goals_made = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    field_goals_attempted = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    field_goal_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    three_pointers_made = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    three_pointers_attempted = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    three_point_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    two_pointers_made = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    two_pointers_attempted = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    two_point_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    effective_field_goal_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    free_throws_made = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    free_throws_attempted = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    free_throw_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    offensive_rebounds = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    defensive_rebounds = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_rebounds = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    assists = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    steals = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    blocks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    turnovers = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    personal_fouls = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    

    def __str__(self):
        return self.name
        
class Rank(models.Model):
    name = models.CharField(max_length=255)
    rank = models.IntegerField(default=0)

    def __str__(self):
        return self.name
