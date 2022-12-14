import imp
from .models import InitialGameObjectiveBayesianNetwork, InitialMainBayesianNetwork, LearningObjectiveTrajectory, UserGameObjectiveBayesianNetwork, UserMainBayesianNetwork
from .resources import InitialGameObjectiveBayesianNetworkResource, InitialMainBayesianNetworkResource, LearningObjectiveTrajectoryResource, UserGameObjectiveBayesianNetworkResource, UserMainBayesianNetworkResource
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

class UserGameObjectiveBayesianNetworkAdmin(ImportExportModelAdmin):
    resource_class = UserGameObjectiveBayesianNetworkResource
admin.site.register(UserGameObjectiveBayesianNetwork, UserGameObjectiveBayesianNetworkAdmin)

class UserMainBayesianNetworkAdmin(ImportExportModelAdmin):
    resource_class = UserMainBayesianNetworkResource
admin.site.register(UserMainBayesianNetwork, UserMainBayesianNetworkAdmin)

class LearningObjectiveTrajectoryAdmin(ImportExportModelAdmin):
    resource_class = LearningObjectiveTrajectoryResource
admin.site.register(LearningObjectiveTrajectory, LearningObjectiveTrajectoryAdmin)

class InitialGameObjectiveBayesianNetworkAdmin(ImportExportModelAdmin):
    resource_class = InitialGameObjectiveBayesianNetworkResource
admin.site.register(InitialGameObjectiveBayesianNetwork, InitialGameObjectiveBayesianNetworkAdmin)

class InitialMainBayesianNetworkAdmin(ImportExportModelAdmin):
    resource_class = InitialMainBayesianNetworkResource
admin.site.register(InitialMainBayesianNetwork, InitialMainBayesianNetworkAdmin)
