from  logic import *
import copy
from itertools import combinations
from sympy.logic.boolalg import And, Or
from sympy.parsing.sympy_parser import parse_expr

def remove_inconsistency(agent, new_belief):
    contracted_belief = copy.copy(agent.KB_strs)
    contract_after = []
    for belief, _ in agent.KB_strs:
        while "<>" in belief:
            sp = belief.split("<>", 1)
            if str(Not(sp[0])) == new_belief:
                contract_after.append(sp[1])
            if str(Not(sp[1])) == new_belief:
                contract_after.append(sp[0])
            belief = sp[1]
    if check_consistency(contracted_belief, new_belief):
        [remove_inconsistency(agent, str(Not(x))) for x in contract_after]
        return contracted_belief
    else:
        for i in range(len(contracted_belief) - 1, 0, -1):
            combs = list(combinations(contracted_belief, i))
            combs.reverse()
            for comb in combs:
                if check_consistency(comb, new_belief):
                    agent.KB_strs = list(comb)
                    [remove_inconsistency(agent, str(Not(x))) for x in contract_after]
                    return comb

    agent.KB_strs = []
    return []
            
    # for i in range(len(agent.KB_strs)):
    #     if not check_consistency([agent.KB_strs[i]], new_belief):
    #         contracted_belief.remove(agent.KB_strs[i])
    # agent.KB_strs = contracted_belief

def contract(agent, new_belief):
    contracted_belief = copy.copy(agent.KB_strs)
    delete_after = []
    add_back = []
    for belief, i in agent.KB_strs:
        ab = True
        while "<>" in belief:
            sp = belief.split("<>", 1)
            if str(sp[0]) == new_belief:
                delete_after.append(sp[1])
            if str(sp[1]) == new_belief:
                delete_after.append(sp[0])
            if ab:
                add_back.append((belief, i))
                agent.KB_strs.remove((belief, i))
                ab = False
            belief = sp[1]
    for i in range(len(agent.KB_strs)):
        if agent.KB_strs[i][0] == new_belief:
            contracted_belief.remove(agent.KB_strs[i])
            agent.KB_strs = contracted_belief
    for d in delete_after:
        contract(agent, d)

    for a in add_back:
        if a not in agent.KB_strs:
            agent.KB_strs.append(a)

    return contracted_belief

def expansion(agent, new_belief):
    expanded_belief = copy.copy(agent.KB_strs)
    new_belief_list = []
    sympy_exp = parse_expr(preprocess_equivalent(new_belief), evaluate=False)
    if isinstance(sympy_exp, And) :
        new_belief_cnf = to_cnf(new_belief).args
        new_belief_list = list(new_belief_cnf)
    else:
        new_belief_list.append(new_belief)
        
    belief_list = []
    for belief, _ in expanded_belief:
        belief_list.append(belief.replace(" ", ""))
        
    for i in new_belief_list:
        if str(i) not in belief_list:
            expanded_belief.append((str(i), agent.kb_num))
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
    new_belief_list = []
    sympy_exp = parse_expr(preprocess_equivalent(new_belief), evaluate=False)
    if isinstance(sympy_exp, And) :
        new_belief_cnf = to_cnf(new_belief).args
        new_belief_list = list(new_belief_cnf)
    else:
        new_belief_list.append(new_belief)
    for i in new_belief_list:
        remove_inconsistency(agent, str(i))
        for belief, _ in agent.KB_strs:
            if isinstance(parse_expr(belief, evaluate=False), Or):
                resolved_belief, is_skipped = resolve(extract_clauses(to_cnf(belief))[0], extract_clauses(to_cnf(i))[0])
                if resolved_belief and not is_skipped:
                    temp = ""
                    for c in resolved_belief:
                        temp += c + '|'
                    resolved_belief = temp[:-1]
                    agent.KB_strs[agent.KB_strs.index((belief, _))] = (resolved_belief, _)
        expansion(agent, str(i))
    return agent.KB_strs
