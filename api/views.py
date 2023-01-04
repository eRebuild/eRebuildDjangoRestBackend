from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView

from bayesianNetwork.level_recommender import RecommendLevels, UpdateLevelRecommendations
from bayesianNetwork.models import UserGameData
from bayesianNetwork.stealth_assessment import PredictGameObjectiveNetwork, PredictMainNetwork
from .serializers import *
from django.shortcuts import render, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')
    elif request.user.is_authenticated:
        return redirect('')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def geeks_view(request):
    if request.user.is_authenticated:
        # create a dictionary to pass
        # data to the template
        context = {
            "token": Token.objects.get_or_create(user=request.user.id)[0],
            "data": "Gfg is the best",
            "list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }
        # return response with template and context
        return render(request, "geeks.html", context)
    else:
        return register(request)

class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register.html'
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GameObjectiveViewSet(viewsets.ModelViewSet):
    queryset = GameObjective.objects.all()
    serializer_class = GameObjectiveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DimensionViewSet(viewsets.ModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ItemQuantityViewSet(viewsets.ModelViewSet):
    queryset = ItemQuantity.objects.all()
    serializer_class = ItemQuantitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LearningObjectiveViewSet(viewsets.ModelViewSet):
    queryset = LearningObjective.objects.all()
    serializer_class = LearningObjectiveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BadgeRequirementViewSet(viewsets.ModelViewSet):
    queryset = BadgeRequirement.objects.all()
    serializer_class = BadgeRequirementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ObjectivePairViewSet(viewsets.ModelViewSet):
    queryset = ObjectivePair.objects.all()
    serializer_class = ObjectivePairSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ObjectiveWeightViewSet(viewsets.ModelViewSet):
    queryset = ObjectiveWeight.objects.all()
    serializer_class = ObjectiveWeightSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LargeResultsSetPagination

class BadgeResultViewSet(viewsets.ModelViewSet):
    queryset = BadgeResult.objects.all()
    serializer_class = BadgeResultSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ObjectiveResponseViewSet(viewsets.ModelViewSet):
    queryset = ObjectiveResponse.objects.all()
    serializer_class = ObjectiveResponseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LevelResultViewSet(viewsets.ModelViewSet):
    queryset = LevelResult.objects.all()
    serializer_class = LevelResultSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self, request, *args, **kwargs):
        level_result: LevelResult = self.create(request, *args, **kwargs)
        print("DASDA")
        objective_responses = level_result.objective_responses.all()
        for objective_response in objective_responses:
            PredictGameObjectiveNetwork(objective_response)
        PredictMainNetwork(level_result)
        UpdateLevelRecommendations(level_result)
        return Response(data=UserGameData.objects.get(User=level_result.user))


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UnitsPlannerViewSet(viewsets.ModelViewSet):
    queryset = UnitsPlanner.objects.all()
    serializer_class = UnitsPlannerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ShapeViewSet(viewsets.ModelViewSet):
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ItemsPlannerViewSet(viewsets.ModelViewSet):
    queryset = ItemsPlanner.objects.all()
    serializer_class = ItemsPlannerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FoldPlannerViewSet(viewsets.ModelViewSet):
    queryset = FoldPlanner.objects.all()
    serializer_class = FoldPlannerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PlacingPlannerViewSet(viewsets.ModelViewSet):
    queryset = PlacingPlanner.objects.all()
    serializer_class = PlacingPlannerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ObjectiveRequirementsViewSet(viewsets.ModelViewSet):
    queryset = ObjectiveRequirements.objects.all()
    serializer_class = ObjectiveRequirementsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]