from revision import *
from sympy.logic.boolalg import simplify_logic
import copy
from agent import Agent

def succces(agent, new_belief):
    # Check if the new belief is already entailed by the belief base
    if entailment(agent.KB_strs, new_belief):
        return "The new belief is already entailed by the belief base."

    test_agent = copy.copy(agent)
    revise(test_agent, new_belief)
    for i in test_agent.KB_strs:
        if i[0] == new_belief:
            return True
    return False

def success_contraction():
    agent: Agent = Agent()

    agent.add_command("a")
    agent.add_command("a>>b")

    agent.delete_command("b")

    print("Success contraction test: " + str(check_consistency(agent.KB_strs, "~b")))


def inclusion(agent, new_belief):
    exp_agent = copy.copy(agent)
    rev_agent = copy.copy(agent)
    exp_belief = expansion(exp_agent, new_belief)
    rev_belief = revise(rev_agent, new_belief)

    if all(elem in exp_belief for elem in rev_belief):
        return True
    return False

def vacuity(agent, new_belief):
    # Check if the new belief is already entailed by the belief base
    if entailment(agent.KB_strs, new_belief):
        return "The new belief is already entailed by the belief base."

    # extract formulas in belief base
    formulas = [i[0] for i in agent.KB_strs]
    # check if the negated new belief is already in the belief base
    if not str(Not(new_belief)) in formulas:
        exp_agent = copy.copy(agent)
        rev_agent = copy.copy(agent)
        exp_belief = expansion(exp_agent, new_belief)
        rev_belief = revise(rev_agent, new_belief)
        return exp_belief == rev_belief
    else:
        return "The negated new belief is already in the knowledge base."

def consistency(agent, new_belief):
    # check consistency of the new belief and the belief base
    if check_consistency(new_formula=new_belief):
        return check_consistency(agent.KB_strs)
    return False

def extentionality(agent, new_belif_a, new_belif_b):
    # Parse the string formulas into sympy expressions
    formula_a = simplify_logic(new_belif_a)
    formula_b = simplify_logic(new_belif_b)
    # Check equivalence
    if formula_a == formula_b:
        a_agent = copy.copy(agent)
        b_agent = copy.copy(agent)
        a_rev = revise(a_agent, new_belif_a)
        b_rev = revise(b_agent, new_belif_b)
        return a_rev == b_rev
    else: 
        return "The two formulas are not equivalent."
        
if __name__ == "__main__":
    success_contraction()

    
