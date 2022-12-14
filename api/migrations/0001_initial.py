# Generated by Django 4.1 on 2022-08-19 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('log_entry', models.CharField(max_length=30)),
                ('credit_weight', models.IntegerField(default=1)),
                ('description', models.CharField(max_length=240)),
            ],
        ),
        migrations.CreateModel(
            name='BadgeRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.badge')),
            ],
        ),
        migrations.CreateModel(
            name='Dimension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('value', models.DecimalField(decimal_places=4, default=1, max_digits=10)),
                ('unit', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GameObjective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=240)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=240)),
                ('cost', models.IntegerField(default=100)),
                ('dimensions', models.ManyToManyField(blank=True, to='api.dimension')),
            ],
        ),
        migrations.CreateModel(
            name='ItemQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.item')),
            ],
        ),
        migrations.CreateModel(
            name='LearningObjective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=240)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=240)),
                ('starting_credits', models.IntegerField(default=1000)),
                ('difficulty_math', models.IntegerField(default=0)),
                ('difficulty_hci', models.IntegerField(default=0)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.area')),
                ('badges', models.ManyToManyField(to='api.badgerequirement')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ObjectivePair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gameobjective')),
                ('learning_objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.learningobjective')),
            ],
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('perimeter_formula', models.CharField(max_length=300)),
                ('area_formula', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=240)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('quantity', models.IntegerField(default=0)),
                ('dimensions', models.ManyToManyField(related_name='unit_dimensions', to='api.dimension')),
                ('units', models.ManyToManyField(blank=True, to='api.unit')),
            ],
        ),
        migrations.CreateModel(
            name='UnitsPlanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.level')),
                ('units', models.ManyToManyField(to='api.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('dimensions', models.ManyToManyField(to='api.dimension')),
                ('shape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.shape')),
            ],
        ),
        migrations.CreateModel(
            name='PlacingPlanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selection_options', models.JSONField()),
                ('expected_input', models.JSONField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.level')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.module')),
            ],
        ),
        migrations.CreateModel(
            name='ObjectiveWeight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=4, default=1, max_digits=10)),
                ('objective_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.objectivepair')),
            ],
        ),
        migrations.AddField(
            model_name='level',
            name='learning_game_objective_weights',
            field=models.ManyToManyField(to='api.objectiveweight'),
        ),
        migrations.AddField(
            model_name='level',
            name='shop_items',
            field=models.ManyToManyField(blank=True, related_name='shop_items', to='api.itemquantity'),
        ),
        migrations.AddField(
            model_name='level',
            name='starting_items',
            field=models.ManyToManyField(blank=True, related_name='starting_items', to='api.itemquantity'),
        ),
        migrations.AddField(
            model_name='level',
            name='tools',
            field=models.ManyToManyField(to='api.tool'),
        ),
        migrations.CreateModel(
            name='ItemsPlanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formula', models.CharField(max_length=300)),
                ('expected_quantity', models.JSONField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.item')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.level')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.module')),
                ('targets', models.ManyToManyField(blank=True, to='api.target')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('dimensions', models.ManyToManyField(related_name='group_dimensions', to='api.dimension')),
                ('units', models.ManyToManyField(to='api.unit')),
            ],
        ),
        migrations.CreateModel(
            name='FoldPlanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=300)),
                ('expected_input', models.JSONField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.level')),
            ],
        ),
    ]
