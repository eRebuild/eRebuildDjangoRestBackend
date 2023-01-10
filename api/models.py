from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Tool(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    def __str__(self):
        return self.name

class Badge(models.Model):
    name = models.CharField(max_length=30)
    log_entry = models.CharField(max_length=30)
    credit_weight = models.IntegerField(default=1)
    description = models.CharField(max_length=240)
    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class GameObjective(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    node_name = models.CharField(blank=True, max_length=64)
    negative_correlation = models.BooleanField()
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    cost = models.IntegerField(default=100)
    def __str__(self):
        return self.name

class Dimension(models.Model):
    name = models.CharField(max_length=30)
    value = models.FloatField(default=1)
    measurement_unit = models.CharField(max_length=30)
    def __str__(self):
        return str(self.name) + ': ' + str(self.value) + str(self.unit)

class ItemDimension(Dimension):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name) + ': ' + str(self.value) + str(self.unit)


class ItemQuantity(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return str(self.item) + ' ' + str(self.quantity) 

class LearningObjective(models.Model):
    name = models.CharField(max_length=30)
    node_name = models.CharField(max_length=30)
    description = models.CharField(max_length=360)
    example = models.CharField(max_length=360, null=True)
    def __str__(self):
        return self.name
    
class ObjectivePair(models.Model):
    game_objective = models.ForeignKey(GameObjective, on_delete=models.CASCADE)
    learning_objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.learning_objective) +' ' + str(self.game_objective)

class Unit(models.Model):
    name = models.CharField(max_length=30)
    quantity = models.IntegerField(default=0)
    units = models.ManyToManyField('self', blank=True)
    def __str__(self):
        return str(self.quantity) + 'x' + str(self.name)

class UnitDimension(Dimension):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name) + ': ' + str(self.value) + str(self.unit)

class Shape(models.Model):
    name = models.CharField(max_length=30, blank=True)
    perimeter_formula = models.CharField(max_length=300, blank=False)
    area_formula = models.CharField(max_length=300, blank=False)
    def __str__(self):
        return str(self.name)

class Target(models.Model):
    name = models.CharField(max_length=30, blank=True)
    shape = models.ForeignKey(Shape, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name)


class TargetDimension(Dimension):
    unit = models.ForeignKey(Target, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name) + ': ' + str(self.value) + str(self.unit)

class Module(models.Model):
    name = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return str(self.name)

class Vector2():
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return f'x:"{self.x:.2f} y:{self.y:.2f}'

class Vector3(Vector2):
    def __init__(self, z):
        super(Vector2, self).__init__()
        self.z = z
    def __str__(self):
        return f'{super(Vector2, self).__str__()} z:{self.z:.2f}'

class Quaternion(Vector3):
    def __init__(self, w):
        super(Vector3, self).__init__()
        self.w = w
    def __str__(self):
        return f'{super(Vector3, self).__str__()} z:{self.w:.2f}'

class Transform():
    def __init__(self, position, rotation, scale):
        self.position = position
        self.rotation = rotation
        self.scale = scale
    def __str__(self):
        return f'{self.position}\n{self.rotation}\n{self.scale}'

class InWorldItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    transform = models.JSONField()
    needs_collection = models.BooleanField()
    is_interactable = models.BooleanField()
    is_ghost = models.BooleanField()
    is_visible = models.BooleanField()
    is_trigger = models.BooleanField()
    keep_apart_group = models.IntegerField(blank=True)
    keep_close_group = models.IntegerField(blank=True)
    paint_needed = models.IntegerField(blank=True)

class Level(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    starting_credits = models.IntegerField(default=1000)
    difficulty_math = models.IntegerField(default=0)
    difficulty_hci = models.IntegerField(default=0)
    tools = models.ManyToManyField(Tool, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shop_items = models.ManyToManyField(ItemQuantity, blank=True, related_name="shop_items")
    starting_items = models.ManyToManyField(ItemQuantity, blank=True, related_name="starting_items")
    prerequesite_levels = models.ManyToManyField('self', blank=True)
    training = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class BadgeRequirement(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="badge_requirements")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    threshold = models.FloatField(default=0)
    def __str__(self):
        return str(self.badge) + ' ' + str(self.threshold)

class ObjectiveRequirements(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="objective_requirements")
    pair = models.ForeignKey(ObjectivePair, on_delete=models.CASCADE)
    weight = models.FloatField(default=1)
    description = models.CharField(blank=True, max_length=240)
    target = models.FloatField(null=True, blank=True)
    tolerance = models.FloatField(null=True, blank=True)
    json = models.JSONField(null=True, blank=True, default=dict)
    result_low_cutoff = models.FloatField(null=True, blank=True)
    result_high_cutoff = models.FloatField(null=True, blank=True)
    time_low_cutoff = models.FloatField(null=True, blank=True)
    time_high_cutoff = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.pair)

class ObjectiveResponse(models.Model):
    requirements = models.ForeignKey(ObjectiveRequirements, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    time = models.FloatField()
    complete = models.BooleanField()
    actual = models.FloatField(null=True, blank=True)
    json = models.JSONField(null=True, blank=True, default=dict);
    date_complete = models.DateTimeField(auto_now_add=True)
    error_message = models.CharField(max_length=300, blank=True)
    def __str__(self):
        return str(self.requirements)

class LevelResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.BooleanField()
    date_complete = models.DateTimeField(auto_now_add=True)

class UnitsPlanner(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    units = models.ManyToManyField(Unit)
    def __str__(self):
        return str(self.level.name)

class ItemsPlanner(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    formula = models.CharField(max_length=300, blank=False)
    targets = models.ManyToManyField(Target, blank=True)
    expected_quantity = models.JSONField()
    def __str__(self):
        return str(self.level.name) + ' ' + str(self.module.name)

class FoldPlanner(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    image = models.CharField(max_length=300, blank=True)
    expected_input = models.JSONField()
    def __str__(self):
        return str(self.level.name)

class PlacingPlanner(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    selection_options = models.JSONField()
    expected_input = models.JSONField()
    def __str__(self):
        return str(self.level.name) + ' ' + str(self.module.name)


class UserGameData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None,related_name="user_temp")
    unlocked_learning_objectives = models.ManyToManyField(LearningObjective, related_name="unlocked_learning_objectives_temp")
    closed_learning_objectives = models.ManyToManyField(LearningObjective, related_name="closed_learning_objectives_temp")
    recommended_levels = models.ManyToManyField(Level, related_name="recommended_levels_temp", blank=True)
    completed_levels = models.ManyToManyField(Level, related_name="completed_levels_temp", blank=True)
    unlocked_levels = models.ManyToManyField(Level, related_name="unlocked_levels_temp", blank=True)
    unlocked_linear_levels = models.ManyToManyField(Level, related_name="unlocked_linear_levels_temp", blank=True)

class BadgeResult(models.Model):
    badge_requirement = models.ForeignKey(BadgeRequirement, on_delete=models.CASCADE)
    user = models.ForeignKey(UserGameData, on_delete=models.CASCADE, related_name='badges')
    awarded = models.BooleanField()
    actual = models.FloatField(null=True, blank=True)
