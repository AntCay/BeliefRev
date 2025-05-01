from  logic import *
import copy
from itertools import combinations

def contract(agent, new_belief):
    contracted_belief = copy.copy(agent.KB_strs)
    if check_consistency(contracted_belief, new_belief):
        return contracted_belief
    else:
        for i in range(len(contracted_belief) - 1, 0, -1):
            combs = list(combinations(contracted_belief, i))
            combs.reverse()
            for comb in combs:
                if check_consistency(comb, new_belief):
                    agent.KB_strs = list(comb)
                    return comb

    agent.KB_strs = []
    return []
            
    # for i in range(len(agent.KB_strs)):
    #     if not check_consistency([agent.KB_strs[i]], new_belief):
    #         contracted_belief.remove(agent.KB_strs[i])
    # agent.KB_strs = contracted_belief

def delete_belief(agent, new_belief):
    contracted_belief = copy.copy(agent.KB_strs)
    for i in range(len(agent.KB_strs)):
        if agent.KB_strs[i][0] == new_belief:
            contracted_belief.remove(agent.KB_strs[i])
    agent.KB_strs = contracted_belief
    return contracted_belief

def expansion(agent, new_belief):
    expanded_belief = copy.copy(agent.KB_strs)

    for belief, _ in expanded_belief:
        if new_belief == belief:
            return expanded_belief

    expanded_belief.append((new_belief, agent.kb_num))
    agent.kb_num += 1
    agent.KB_strs = expanded_belief
    return expanded_belief

def revise(agent, new_belief):
    # Check if the new belief is already entailed by the belief base
    # if entailment(agent.KB_strs, new_belief):
    #     return agent.KB_strs  # No changes needed
    #
    # # If the new belief is inconsistent, contract and expand
    # if not check_consistency(agent.KB_strs, new_belief):
    #     contract(agent, new_belief)
    #     expansion(agent, new_belief)
    #     return agent.KB_strs
    #
    # # If the new belief is not entailed and consistent, expand the belief base
    # formulas = [i[0] for i in agent.KB_strs]
    # if not new_belief == "" and not new_belief in formulas:
    #     expansion(agent, new_belief)
    # return agent.KB_strs
    contract(agent, new_belief)
    expansion(agent, new_belief)
    return agent.KB_strs
