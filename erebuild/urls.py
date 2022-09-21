from django.urls import include, path
from rest_framework import routers
from api import views
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'User', views.UserViewSet)
router.register(r'Group', views.GroupViewSet)
router.register(r'Tool', views.ToolViewSet)
router.register(r'Badge', views.BadgeViewSet)
router.register(r'Area', views.AreaViewSet)
router.register(r'GameObjective', views.GameObjectiveViewSet)
router.register(r'Dimension', views.DimensionViewSet)
router.register(r'Item', views.ItemViewSet)
items_router = routers.NestedSimpleRouter(router, r'Item', lookup='dimensions')
items_router.register(r'Dimension', views.DimensionViewSet)
router.register(r'ItemQuantity', views.ItemQuantityViewSet)
router.register(r'LearningObjective', views.LearningObjectiveViewSet)
router.register(r'BadgeRequirement', views.BadgeRequirementViewSet)
router.register(r'ObjectivePair', views.ObjectivePairViewSet)
router.register(r'ObjectiveWeight', views.ObjectiveWeightViewSet)
router.register(r'Level', views.LevelViewSet)
router.register(r'Unit', views.UnitViewSet)
router.register(r'UnitsPlanner', views.UnitsPlannerViewSet)
router.register(r'Shape', views.ShapeViewSet)
router.register(r'Target', views.TargetViewSet)
router.register(r'Module', views.ModuleViewSet)
router.register(r'ItemsPlanner', views.ItemsPlannerViewSet)
router.register(r'FoldPlanner', views.FoldPlannerViewSet)
router.register(r'PlacingPlanner', views.PlacingPlannerViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(items_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),
    path('', views.geeks_view),
]

urlpatterns  +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
