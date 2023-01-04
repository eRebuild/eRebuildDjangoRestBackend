from operator import index
from api.models import LearningObjective, LevelResult, User
from bayesianNetwork.models import LearningObjectiveTrajectory, UserGameData
from bayesianNetwork.stealth_assessment import GetNodeScore


def ChangeRecommendedLevel(old_level, new_level, recommended_levels):
    try:
        recommended_levels.remove(old_level)
    except:
        pass
    try:
        recommended_levels.add(new_level)
    except:
        pass


def UpdateLevelRecommendations(level_result: LevelResult):
    try:
        user: UserGameData = UserGameData.objects.get(user=level_result.user)
    except:
        default_user: User =  User.objects.get(username="default")
        default_game_data: UserGameData = UserGameData.objects.get(user=default_user)
        user: UserGameData = UserGameData.objects.create(
            user=level_result.user,
        )
        user.closed_learning_objectives.set(default_game_data.closed_learning_objectives.all())
        user.unlocked_learning_objectives.set(default_game_data.unlocked_learning_objectives.all())
    learning_objectives_updated = False
    recommend_levels = user.recommended_levels
    for learning_objective in user.unlocked_learning_objectives.all():
        score: str = GetNodeScore(learning_objective.node_name, user.user)
        levels, num_total = GetUnlockedLevelsForLearningObjective(learning_objective, user)
        num_unlocked = len(levels)
        if level_result.level in recommend_levels:
            if level_result.completed:
                if num_unlocked == 0 or (score == 'M' or score == 'H' and num_total - num_unlocked >= 2):
                    user.closed_learning_objectives.add(learning_objective)
                    learning_objectives_updated |= True
                else:
                    i = index(levels, level_result.level) + 1
                    if i < num_unlocked:
                        ChangeRecommendedLevel(level_result.level, levels[i], recommend_levels)
            else:
                i = index(levels, level_result.level) - 1
                if i >= 0:
                    ChangeRecommendedLevel(
                        level_result.level, levels[i], recommend_levels)
    if learning_objectives_updated:
        graph = LearningObjectiveTrajectory.objects.latest('date_modified')
        for node in graph.nodes():
            if all(elem in user.closed_learning_objectives for elem in list(graph.successors(node))) and node not in user.closed_learning_objectives:
                user.unlocked_learning_objectives.add(LearningObjective.objects.get(node_name=node.name))
        recommended_levels, unlocked_levels = RecommendLevels()
        user.recommended_levels.set(recommend_levels, clear=True)
        user.unlocked_levels.add(unlocked_levels)
    user.save()


def GetUnlockedLevelsForLearningObjective(learning_objective: LearningObjective, user: UserGameData):
    mathching_unlocked_levels = []
    count = 0
    for level in user.unlocked_levels.all():
        learning_objectives = [
            objective_weight.objective_pair.learning_objective for objective_weight in level.objective_weights]
        if learning_objective in learning_objectives:
            count += 1
        if all(learning_objective in user.closed_learning_objectives or learning_objective in user.unlockec_learning_objectives for learning_objective in learning_objectives):
            mathching_unlocked_levels.append(level)
    mathching_unlocked_levels.sort(key=lambda l: l.difficulty_math)
    return mathching_unlocked_levels, count


def RecommendLevels(user: UserGameData):
    recommend_levels = []
    all_unlocked_levels = set()

    for learning_objective in user.unlocked_learning_objectives:
        levels = GetUnlockedLevelsForLearningObjective(learning_objective, user)
        all_unlocked_levels.update(levels)
        if len(levels) > 0:
            recommend_levels.append(levels[len(levels)//2])
