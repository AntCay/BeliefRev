from revision import *
from sympy.logic.boolalg import simplify_logic
import copy
from agent import Agent

def succces_revision():
    test_agent = Agent()
    test_agent.expand_command("p")
    test_agent.expand_command("p>>q")
    new_belief = "q"
    
    test_agent.revise_command(new_belief)
    
    for i in test_agent.KB_strs:
        if i[0] == new_belief:
            return print("Success revision test: " + str(True))
    return print("Success revision test: " + str(False))

def success_contraction():
    agent: Agent = Agent()

    agent.expand_command("a")
    agent.expand_command("a>>b")

    agent.contract_command("b")

    print("Success contraction test: " + str(not includes_clause_in_closure_of_knowledge_base(agent, "b")))

def inclusion_revision():
    agent = Agent()
    
    agent.expand_command("p")
    agent.expand_command("p>>q")
    new_belief = "q"
    
    exp_agent = copy.copy(agent)
    rev_agent = copy.copy(agent)
    exp_agent.expand_command(new_belief)
    rev_agent.revise_command(new_belief)

    print("Inclusion revision test: " + str(all(elem in exp_agent.KB_strs for elem in rev_agent.KB_strs)))

def inclusion_contraction():
    agent: Agent = Agent()

    agent.expand_command("a")
    agent.expand_command("a>>b")
    agent.expand_command("c")

    before_kb = set(agent.KB_strs)

    agent.contract_command("b")
    
    after_kb = set(agent.KB_strs)

    print("Inclusion contraction test: " + str(after_kb.issubset(before_kb)))

def vacuity_revision():
    agent = Agent()
    
    agent.expand_command("p")
    agent.expand_command("p>>q")
    new_belief = "q"
    
    # extract formulas in belief base
    formulas = [i[0] for i in agent.KB_strs]
    
    # check if the negated new belief is already in the belief base
    if not str(Not(new_belief)) in formulas:
        exp_agent = copy.copy(agent)
        rev_agent = copy.copy(agent)
        exp_agent.expand_command(new_belief)
        rev_agent.revise_command(new_belief)
        return print("Vacuity Revision test : " + str(exp_agent.KB_strs == rev_agent.KB_strs))
    else:
        return print("Vacuity Revision test: The negated new belief is already in the knowledge base.")

def vacuity_contraction():
    agent: Agent = Agent()

    agent.expand_command("a")
    agent.expand_command("a>>b")
    agent.expand_command("c")

    before_kb = agent.KB_strs

    agent.contract_command("d")

    after_kb = agent.KB_strs

    print("Vacuity contraction test: " + str(before_kb == after_kb))


def consistency_revision():
    agent = Agent()
    
    agent.expand_command("p")
    agent.expand_command("p>>q")
    new_belief = "q"
    
    # check consistency of the new belief and the belief base
    if check_consistency(new_formula=new_belief):
        print("Consistency revision test: "  + str(check_consistency(agent.KB_strs)))


def extentionality_revision():
    agent = Agent()
    
    agent.expand_command("a")
    agent.expand_command("c")
    agent.expand_command("a>>b")
    agent.expand_command("a<>c")
    new_belief_a = "a"
    new_belief_b = "c"
    
    a_agent = copy.copy(agent)
    b_agent = copy.copy(agent)
    a_agent.revise_command(new_belief_a)
    b_agent.revise_command(new_belief_b)
    print("Extentionality revision test: " + str(a_agent.KB_strs == b_agent.KB_strs))

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
    succces_revision()
    inclusion_revision()
    vacuity_revision()
    consistency_revision()
    extentionality_revision()

    
