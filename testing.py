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

    agent.expand_command("a")
    agent.expand_command("a>>b")

    agent.contract_command("b")

    print("Success contraction test: " + str(not includes_clause_in_closure_of_knowledge_base(agent, "b")))

def inclusion(agent, new_belief):
    exp_agent = copy.copy(agent)
    rev_agent = copy.copy(agent)
    exp_belief = expansion(exp_agent, new_belief)
    rev_belief = revise(rev_agent, new_belief)

    if all(elem in exp_belief for elem in rev_belief):
        return True
    return False

def inclusion_contraction():
    agent: Agent = Agent()

    agent.expand_command("a")
    agent.expand_command("a>>b")
    agent.expand_command("c")

    before_kb = set(agent.KB_strs)

    agent.contract_command("b")
    
    after_kb = set(agent.KB_strs)

    print("Inclusion contraction test: " + str(after_kb.issubset(before_kb)))

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

def vacuity_contraction():
    agent: Agent = Agent()

    agent.expand_command("a")
    agent.expand_command("a>>b")
    agent.expand_command("c")

    before_kb = agent.KB_strs

    agent.contract_command("d")

    after_kb = agent.KB_strs

    print("Vacuity contraction test: " + str(before_kb == after_kb))


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

def extentionality_contraction():
    agentA: Agent = Agent()
    agentC: Agent = Agent()

    agentA.expand_command("a")
    agentA.expand_command("c")
    agentA.expand_command("a>>b")
    agentA.expand_command("a<>c")
    agentA.contract_command("a")
    contract_A_kb = agentA.KB_strs

    agentC.expand_command("a")
    agentC.expand_command("c")
    agentC.expand_command("a>>b")
    agentC.expand_command("a<>c")
    agentC.contract_command("c")
    contract_C_kb = agentC.KB_strs

    print("Extentionality contraction test: " + str(contract_A_kb == contract_C_kb))


# HELPER FUNCTIONS:
def includes_clause_in_closure_of_knowledge_base(agent, clause):
    return not check_consistency(agent.KB_strs, str(Not(clause)))

if __name__ == "__main__":
    success_contraction()
    inclusion_contraction()
    vacuity_contraction()
    extentionality_contraction()

    
