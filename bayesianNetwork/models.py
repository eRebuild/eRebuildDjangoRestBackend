from django.db import models
from api.models import GameObjective, LearningObjective, Level, User


class UserGameObjectiveBayesianNetwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    game_objective = models.ForeignKey(GameObjective, on_delete=models.CASCADE, default=None)
    network = models.JSONField(null=True, blank=True, default=dict)
    score = models.CharField(max_length=1, default='M')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'game_objective'], name='name_game_objective')
        ]

class UserMainBayesianNetwork(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    network = models.JSONField(null=True, blank=True, default=dict)
    score = models.CharField(max_length=1, default='M')

class LearningObjectiveTrajectory(models.Model):
    graph = models.JSONField(null=True, blank=True, default=dict)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)


class InitialGameObjectiveBayesianNetwork(models.Model):
    game_objective = models.OneToOneField(GameObjective, on_delete=models.CASCADE, default=None)
    graph = models.JSONField(null=True, blank=True, default=dict)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)


class InitialMainBayesianNetwork(models.Model):
    graph = models.JSONField(null=True, blank=True, default=dict)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
