from import_export.resources import ModelResource
from .models import *


class UserGameObjectiveBayesianNetworkResource(ModelResource):
    class Meta:
        model = UserGameObjectiveBayesianNetwork


class UserMainBayesianNetworkResource(ModelResource):
    class Meta:
        model = UserMainBayesianNetwork


class LearningObjectiveTrajectoryResource(ModelResource):
    class Meta:
        model = LearningObjectiveTrajectory


class InitialGameObjectiveBayesianNetworkResource(ModelResource):
    class Meta:
        model = UserMainBayesianNetwork


class InitialMainBayesianNetworkResource(ModelResource):
    class Meta:
        model = UserMainBayesianNetwork
