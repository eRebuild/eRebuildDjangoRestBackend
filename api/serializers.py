from django.contrib.auth.models import User, Group
from rest_framework import serializers

from bayesianNetwork.level_recommender import UpdateLevelRecommendations
from bayesianNetwork.stealth_assessment import PredictGameObjectiveNetwork, PredictMainNetwork
from .models import *


class HyperlinkedIdModelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    #remember_me = serializers.BooleanField()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password")

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ToolSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'


class BadgeSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'


class AreaSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class GameObjectiveSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = GameObjective
        fields = '__all__'


class DimensionSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Dimension
        fields = '__all__'


class ItemSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ItemQuantitySerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = ItemQuantity
        fields = '__all__'


class LearningObjectiveSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = LearningObjective
        fields = '__all__'


class BadgeRequirementSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        depth = 2
        model = BadgeRequirement
        fields = [
            'url',
            'badge',
            'threshold',
            'level',
        ]

class ObjectivePairSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = ObjectivePair
        fields = '__all__'

class LevelResultSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = LevelResult
        fields = '__all__'
    def create(self, validated_data):
        level_result : LevelResult = LevelResult.objects.create(**validated_data)
        objective_responses = ObjectiveResponse.objects.filter(user=level_result.user, requirements__level=level_result.level)
        for objective_response in objective_responses:
            PredictGameObjectiveNetwork(objective_response)
        PredictMainNetwork(level_result)
        UpdateLevelRecommendations(level_result)
        return level_result

class BadgeResultSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = BadgeResult
        depth = 2
        fields = [
            'badge_requirement',
            'awarded',
        ]
    
class ObjectiveRequirementsSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = ObjectiveRequirements
        depth = 3
        fields = [
            'id',
            'url',
            'pair',
            'weight',
            'description',
            'target',
            'tolerance',
            'json',
            'result_low_cutoff',
            'result_high_cutoff',
            'time_low_cutoff',
            'time_high_cutoff',
        ]

class ObjectiveResponseSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = ObjectiveResponse
        fields = '__all__'


class LevelSerializer(HyperlinkedIdModelSerializer):
    objective_requirements = ObjectiveRequirementsSerializer(many=True, read_only=True)
    badge_requirements = BadgeRequirementSerializer(many=True, read_only=True)
    class Meta:
        model = Level
        depth = 6
        fields = [
            'id',
            'url',
            'name',
            'description',
            'starting_credits',
            'difficulty_math',
            'difficulty_hci' ,
            'tools',
            'area',
            'creator',
            'shop_items',
            'starting_items',
            'objective_requirements',
            'badge_requirements',
            'training',
            'prerequesite_levels'
        ]

class UnitSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class UnitsPlannerSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = UnitsPlanner
        fields = '__all__'

class ShapeSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Shape
        fields = '__all__'


class TargetSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Target
        fields = '__all__'


class ModuleSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class ItemsPlannerSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = ItemsPlanner
        fields = '__all__'



class FoldPlannerSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = FoldPlanner
        fields = '__all__'


class PlacingPlannerSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = PlacingPlanner
        fields = '__all__'


class UserGameDataSerializer(HyperlinkedIdModelSerializer):
    awarded_badges = BadgeResultSerializer(many=True, read_only=True)
    class Meta:
        model = UserGameData
        depth = 3
        fields = [
            'user',
            'user_id',
            'unlocked_learning_objectives',
            'closed_learning_objectives',
            'recommended_levels',
            'completed_levels',
            'unlocked_levels',
            'unlocked_linear_levels',
            'awarded_badges',
        ]
