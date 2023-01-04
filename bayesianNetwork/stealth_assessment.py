from pomegranate import BayesianNetwork

from api.models import LevelResult, ObjectiveResponse
from .models import InitialGameObjectiveBayesianNetwork, InitialMainBayesianNetwork, UserGameObjectiveBayesianNetwork, UserMainBayesianNetwork
from django.core.exceptions import ObjectDoesNotExist

def ConvertResponseToCategotical(objectiveResponse: ObjectiveResponse):
    cat = {}
    cat['Complete'] = 'T' if objectiveResponse.complete else 'F'
    cat['Time'] = 'H' if objectiveResponse.time <= objectiveResponse.requirements.time_high_cutoff else \
        'M' if objectiveResponse.time <= objectiveResponse.requirements.time_low_cutoff else 'L'
    if objectiveResponse.requirements.type.negative_correlation:
        cat[objectiveResponse.requirements.type.node_name] = 'H' if objectiveResponse.actual <= objectiveResponse.requirements.result_high_cutoff else \
            'M' if objectiveResponse.actual <= objectiveResponse.requirements.result_low_cutoff else 'L'
    else:
        cat[objectiveResponse.requirements.type.node_name] = 'H' if objectiveResponse.actual >= objectiveResponse.requirements.result_high_cutoff else \
            'M' if objectiveResponse.actual >= objectiveResponse.requirements.result_low_cutoff else 'L'
    return cat


def GetNodeScore(node_name, user):
    entry = UserMainBayesianNetwork.objects.get(user=user)
    network = BayesianNetwork.from_dict(entry.network)
    beliefs = network.predict_proba({})
    index = [network.states.index(state) for state in network.states if state.name == node_name]
    scores = beliefs[index][0].parameters[0]
    return max(scores, key=scores.get)


def PredictGameObjectiveNetwork(objectiveResponse: ObjectiveResponse):
    type = objectiveResponse.requirements.type
    try:
        entry = UserGameObjectiveBayesianNetwork.objects.get(user=objectiveResponse.user, gameObjective=type)
    except:
        network = InitialGameObjectiveBayesianNetwork.objects.filter(game_objective=type).latest('date_modified').graph
        entry = UserGameObjectiveBayesianNetwork.objects.create(user=objectiveResponse.user, network=network)
    cat = ConvertResponseToCategotical(objectiveResponse)
    network = BayesianNetwork.from_dict(entry.network)
    entry.score = network.predict_proba(cat)[-1]
    data = [cat[type] if type in cat else None for type in network.states]
    data = network.predict([data])
    network = network.fit(data, inertia=0.925)
    entry.network = network.to_dict()
    entry.save()


def PredictMainNetwork(level_result: LevelResult):
    try:
        entry = UserMainBayesianNetwork.objects.get(user=level_result.user)
    except:
        graph = InitialMainBayesianNetwork.objects.latest('date_modified').graph
        entry = UserMainBayesianNetwork.objects.create(user=level_result.user, network=graph)
        entry.save()
    network = BayesianNetwork.from_dict(entry.network)
    objective_weights = level_result.level.objective_weights.all()
    unique_weights = set(
        [float(objective_weight.weight) for objective_weight in objective_weights])
    data = {}
    math_belief = network.predict_proba(data)[-1].parameters[-1]
    math_score = max(math_belief, key=math_belief.get)
    for weight in unique_weights:
        objective_pairs = [objective_weight.objective_pair for objective_weight in objective_weights if objective_weight.weight == weight]
        for objective_pair in objective_pairs:
            key = "@".join([objective_pair.game_objective.name, objective_pair.learning_objective.name])
            try:
                game_objective_network = UserGameObjectiveBayesianNetwork.objects.get(
                    user=level_result.user, gameObjective=objective_pair.game_objective)
                data[weight] = {key, game_objective_network.score}
                data[weight] = [data[weight][k] if k.name in data[weight]
                    else None for k in network.states]
                data[weight][-1] = math_score
            except ObjectDoesNotExist:
                pass
    if len(data) > 0:
        network.fit(list(data.values()), list(data.keys()), inertia=0.925)
        entry.network = network.to_dict()
        entry.save()
