from operator import itemgetter
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class HyperlinkedIdModelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'url']


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
        model = BadgeRequirement
        fields = '__all__'


class ObjectivePairSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = ObjectivePair
        fields = '__all__'


class ObjectiveWeightSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = ObjectiveWeight
        fields = '__all__'


class LevelSerializer(HyperlinkedIdModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

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
