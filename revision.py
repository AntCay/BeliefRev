from  logic import *
import copy

def contract(agent, new_belief):
    contracted_belief = copy.copy(agent.KB_strs)
    for i in range(len(agent.KB_strs)):
        if not check_consistency([agent.KB_strs[i]], new_belief):
            contracted_belief.remove(agent.KB_strs[i])
    agent.KB_strs = contracted_belief
    return contracted_belief

def expansion(agent, new_belief):
    expanded_belief = copy.copy(agent.KB_strs)
    if not new_belief in agent.KB_strs[0]:
        expanded_belief.append((new_belief, agent.kb_num))
        agent.KB_strs = expanded_belief
        agent.kb_num += 1
    return expanded_belief

def revise(agent, new_belief):
    # Check if the new belief is already entailed by the belief base
    if entailment(agent.KB_strs, new_belief):
        return agent.KB_strs  # No changes needed

    # If the new belief is inconsistent, contract and expand
    if not check_consistency(agent.KB_strs, new_belief):
        contract(agent, new_belief)
        expansion(agent, new_belief)
        return agent.KB_strs

    # If the new belief is not entailed and consistent, expand the belief base
    formulas = [i[0] for i in agent.KB_strs]
    if not new_belief == "" and not new_belief in formulas:
        expansion(agent, new_belief)
    return agent.KB_strs