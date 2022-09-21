from operator import mod, truediv
from pyexpat import model
from statistics import mode
from tkinter import CASCADE, Scale
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
    def __str__(self):
        return self.name

class Dimension(models.Model):
    name = models.CharField(max_length=30)
    value = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    unit = models.CharField(max_length=30)
    def __str__(self):
        return str(self.name) + ': ' + str(self.value) + str(self.unit)

class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    cost = models.IntegerField(default=100)
    dimensions = models.ManyToManyField(Dimension, blank=True)
    def __str__(self):
        return self.name

class ItemQuantity(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return str(self.item) + ' ' + str(self.quantity) 

class LearningObjective(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=360)
    example = models.CharField(max_length=360, null=True)
    def __str__(self):
        return self.name
    
class BadgeRequirement(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    threshold = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    def __str__(self):
        return str(self.badge) + ' ' + str(self.threshold)

class ObjectivePair(models.Model):
    game_objective = models.ForeignKey(GameObjective, on_delete=models.CASCADE)
    learning_objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.learning_objective) +' ' + str(self.game_objective)

class ObjectiveWeight(models.Model):
    objective_pair = models.ForeignKey(ObjectivePair, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    def __str__(self):
        return str(self.objective_pair) + ' ' + str(self.weight)

class Level(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    starting_credits = models.IntegerField(default=1000)
    difficulty_math = models.IntegerField(default=0)
    difficulty_hci = models.IntegerField(default=0)
    tools = models.ManyToManyField(Tool)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    badges = models.ManyToManyField(BadgeRequirement)
    objective_weights = models.ManyToManyField(ObjectiveWeight)
    shop_items = models.ManyToManyField(ItemQuantity, blank=True, related_name="shop_items")
    starting_items = models.ManyToManyField(ItemQuantity, blank=True, related_name="starting_items")
    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=30)
    dimensions = models.ManyToManyField(Dimension, blank=False, related_name="unit_dimensions")
    quantity = models.IntegerField(default=0)
    units = models.ManyToManyField('self', blank=True)
    def __str__(self):
        return str(self.quantity) + 'x' + str(self.name)

class Group(models.Model):
    name = models.CharField(max_length=30, blank=True)
    units = models.ManyToManyField(Unit)
    dimensions = models.ManyToManyField(Dimension, blank=False, related_name="group_dimensions")
    def __str__(self):
        return str(self.name)

class UnitsPlanner(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    units = models.ManyToManyField(Unit)
    def __str__(self):
        return str(self.level.name)

class Shape(models.Model):
    name = models.CharField(max_length=30, blank=True)
    perimeter_formula = models.CharField(max_length=300, blank=False)
    area_formula = models.CharField(max_length=300, blank=False)
    def __str__(self):
        return str(self.name)

class Target(models.Model):
    name = models.CharField(max_length=30, blank=True)
    shape = models.ForeignKey(Shape, on_delete=models.CASCADE)
    dimensions = models.ManyToManyField(Dimension, blank=False)
    def __str__(self):
        return str(self.name)

class Module(models.Model):
    name = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return str(self.name)

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

class ObjectiveRequirements(models.Model):
    type = models.ForeignKey(GameObjective, on_delete=models.CASCADE)
    description = models.CharField(blank=True, max_length=240)
    target = models.FloatField(blank=True)
    tolerance = models.FloatField(blank=True)
    json = models.JSONField()
    def __str__(self):
        return

class ObjectiveResponse(models.Model):
    requirements = models.ForeignKey(ObjectiveRequirements, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    totalTime = models.FloatField()
    complete = models.BooleanField()
    actual = models.FloatField(blank=True)
    json = models.JSONField();
    def __str__(self):
        return

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

