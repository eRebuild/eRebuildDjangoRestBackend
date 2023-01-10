from ast import Mod
from django.contrib import admin
from .models import *
from rest_framework.authtoken.admin import TokenAdmin
from import_export.admin import ImportExportModelAdmin
from .resources import * 


class ShopItemInline(admin.TabularInline):
    model = ShopItemQuantity

class StartingItemInline(admin.TabularInline):
    model = StartingItemQuantity

class InWorldItemInline(admin.TabularInline):
    model = InWorldItem

class BadgeRequirementInline(admin.TabularInline):
    model = BadgeRequirement

class ObjectiveRequirementsInline(admin.TabularInline):
    model = ObjectiveRequirements

class LevelAdmin(ImportExportModelAdmin):
    inlines = [
        ShopItemInline,
        StartingItemInline,
        ObjectiveRequirementsInline,
        BadgeRequirementInline,
        InWorldItemInline,
    ]
    resource_class = LevelResource
admin.site.register(Level, LevelAdmin)

class ToolAdmin(ImportExportModelAdmin):
    resource_class = ToolResource
admin.site.register(Tool, ToolAdmin)

class BadgeAdmin(ImportExportModelAdmin):
    resource_class = BadgeResource
admin.site.register(Badge, BadgeAdmin)


class AreaAdmin(ImportExportModelAdmin):
    resource_class = AreaResource
admin.site.register(Area, AreaAdmin)


class GameObjectiveAdmin(ImportExportModelAdmin):
    resource_class = GameObjectiveResource
admin.site.register(GameObjective, GameObjectiveAdmin)


class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource
admin.site.register(Item, ItemAdmin)

class ItemQuantityAdmin(ImportExportModelAdmin):
    resource_class = ItemQuantityResource
    
admin.site.register(ItemQuantity, ItemQuantityAdmin)


class LearningObjectiveAdmin(ImportExportModelAdmin):
    resource_class = LearningObjectiveResource
admin.site.register(LearningObjective, LearningObjectiveAdmin)




class BadgeRequirementAdmin(ImportExportModelAdmin):
    resource_class = BadgeRequirementResource
admin.site.register(BadgeRequirement, BadgeRequirementAdmin)

class ObjectivePairAdmin(ImportExportModelAdmin):
    resource_class = ObjectivePairResource
admin.site.register(ObjectivePair, ObjectivePairAdmin)

class DimensionAdmin(ImportExportModelAdmin):
    resource_class = DimensionResource
admin.site.register(Dimension, DimensionAdmin)

class UnitAdmin(ImportExportModelAdmin):
    resource_class = UnitResource
admin.site.register(Unit, UnitAdmin)

class UnitsPlannerAdmin(ImportExportModelAdmin):
    resource_class = UnitsPlannerResource
admin.site.register(UnitsPlanner, UnitsPlannerAdmin)

class ShapeAdmin(ImportExportModelAdmin):
    resource_class = ShapeResource
admin.site.register(Shape, ShapeAdmin)

class TargetAdmin(ImportExportModelAdmin):
    resource_class = TargetResource
admin.site.register(Target, TargetAdmin)

class ModuleAdmin(ImportExportModelAdmin):
    resource_class = ModuleResource
admin.site.register(Module, ModuleAdmin)

class ItemsPlannerAdmin(ImportExportModelAdmin):
    resource_class = ItemsPlannerResource
admin.site.register(ItemsPlanner, ItemsPlannerAdmin)

class FoldPlannerAdmin(ImportExportModelAdmin):
    resource_class = FoldPlannerResource
admin.site.register(FoldPlanner, FoldPlannerAdmin)

class PlacingPlannerAdmin(ImportExportModelAdmin):
    resource_class = PlacingPlannerResource
admin.site.register(PlacingPlanner, PlacingPlannerAdmin)

class ObjectiveRequirementsAdmin(ImportExportModelAdmin):
    resource_class = ObjectiveRequirementsResource
admin.site.register(ObjectiveRequirements, ObjectiveRequirementsAdmin)

class LevelResultAdmin(ImportExportModelAdmin):
    resource_class = LevelResultResource
admin.site.register(LevelResult, LevelResultAdmin)

class ObjectiveResponseAdmin(ImportExportModelAdmin):
    resource_class = ObjectiveResponseResource
admin.site.register(ObjectiveResponse, ObjectiveResponseAdmin)

class BadgeResultAdmin(ImportExportModelAdmin):
    resource_class = BadgeResultResource
admin.site.register(BadgeResult, BadgeResultAdmin)

class UserGameDataAdmin(ImportExportModelAdmin):
    resource_class = UserGameDataResource
admin.site.register(UserGameData, UserGameDataAdmin)

# Register your models here.
# admin.site.register(Badge)
# admin.site.register(Area)
# admin.site.register(GameObjective)
# admin.site.register(Item)
# admin.site.register(ItemQuantity)
# admin.site.register(LearningObjective)
# admin.site.register(Level)
# admin.site.register(BadgeRequirement)
# admin.site.register(ObjectivePair)
# admin.site.register(ObjectiveWeight)
# admin.site.register(Dimension)
# admin.site.register(Unit)
# admin.site.register(UnitsPlanner)
# admin.site.register(Shape)
# admin.site.register(Target)
# admin.site.register(Module)
# admin.site.register(ItemsPlanner)
# admin.site.register(FoldPlanner)
# admin.site.register(PlacingPlanner)