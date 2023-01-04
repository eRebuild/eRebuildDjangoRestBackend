from django.contrib.auth.models import User
from api.models import LevelResult
from bayesianNetwork.level_recommender import UpdateLevelRecommendations
from bayesianNetwork.stealth_assessment import PredictGameObjectiveNetwork, PredictMainNetwork
from bayesianNetwork.models import *

user : User = User.objects.get(username="dan")
level_result : LevelResult= LevelResult.objects.get(user=user)

objective_responses = level_result.objective_responses.all()
for objective_response in objective_responses:
    PredictGameObjectiveNetwork(objective_response)


PredictMainNetwork(level_result)
UpdateLevelRecommendations(level_result)