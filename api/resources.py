from import_export.resources import ModelResource
from .models import *

        
class ToolResource(ModelResource):
    class Meta:
        model = Tool


class BadgeResource(ModelResource):
    class Meta:
        model = Badge



class AreaResource(ModelResource):
    class Meta:
        model = Area



class GameObjectiveResource(ModelResource):
    class Meta:
        model = GameObjective



class DimensionResource(ModelResource):
    class Meta:
        model = Dimension



class ItemResource(ModelResource):
    class Meta:
        model = Item



class ItemQuantityResource(ModelResource):
    class Meta:
        model = ItemQuantity



class LearningObjectiveResource(ModelResource):
    class Meta:
        model = LearningObjective



class BadgeRequirementResource(ModelResource):
    class Meta:
        model = BadgeRequirement



class ObjectivePairResource(ModelResource):
    class Meta:
        model = ObjectivePair



class ObjectiveWeightResource(ModelResource):
    class Meta:
        model = ObjectiveWeight



class LevelResource(ModelResource):
    class Meta:
        model = Level


class UnitResource(ModelResource):
    class Meta:
        model = Unit


class UnitsPlannerResource(ModelResource):
    class Meta:
        model = UnitsPlanner


class ShapeResource(ModelResource):
    class Meta:
        model = Shape



class TargetResource(ModelResource):
    class Meta:
        model = Target



class ModuleResource(ModelResource):
    class Meta:
        model = Module



class ItemsPlannerResource(ModelResource):
    class Meta:
        model = ItemsPlanner




class FoldPlannerResource(ModelResource):
    class Meta:
        model = FoldPlanner



class PlacingPlannerResource(ModelResource):
    class Meta:
        model = PlacingPlanner

