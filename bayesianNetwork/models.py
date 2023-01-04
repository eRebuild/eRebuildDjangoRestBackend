from django.db import models
from api.models import GameObjective, LearningObjective, Level, User


class UserGameObjectiveBayesianNetwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    gameObjective = models.ManyToManyField(GameObjective)
    network = models.JSONField(null=True, blank=True, default=dict)
    score = models.CharField(max_length=1, default='M')


class UserMainBayesianNetwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    network = models.JSONField(null=True, blank=True, default=dict)
    score = models.CharField(max_length=1, default='M')


class UserGameData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    unlocked_learning_objectives = models.ManyToManyField(LearningObjective, related_name="unlocked_learning_objectives")
    closed_learning_objectives = models.ManyToManyField(LearningObjective, related_name="closed_learning_objectives")
    recommended_levels = models.ManyToManyField(Level, related_name="recommended_levels", blank=True)
    completed_levels = models.ManyToManyField(Level, related_name="completed_levels", blank=True)
    unlocked_levels = models.ManyToManyField(Level, related_name="unlocked_levels", blank=True)


class LearningObjectiveTrajectory(models.Model):
    graph = models.JSONField(null=True, blank=True, default=dict)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)


class InitialGameObjectiveBayesianNetwork(models.Model):
    game_objective = models.ForeignKey(GameObjective, on_delete=models.CASCADE, default=None)
    graph = models.JSONField(null=True, blank=True, default=dict)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)


class InitialMainBayesianNetwork(models.Model):
    graph = models.JSONField(null=True, blank=True, default=dict)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
