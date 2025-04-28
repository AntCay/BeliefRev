from sympy import symbols
from sympy.logic.boolalg import to_cnf, Implies, Or, And, Not, Equivalent
import itertools
import copy

def preprocess_equivalent(expr_str):
    if '<>' in expr_str:
        x = expr_str.find("<>")
        return "Equivalent("+ preprocess_equivalent(expr_str[:x]) + "," + preprocess_equivalent(expr_str[x+2:]) + ")"
    else:
        return expr_str

def extract_clauses(expr):
    """Extract clauses and literals from a CNF expression as a list of lists."""
    
    def extract_literals(clause):
        """Helper function to extract literals from an 'Or' clause."""
        literals = []
        for term in clause.args:
            if isinstance(term, Not):
                literals.append("~" + str(term.args[0]))
            else:
                literals.append(str(term))
        return literals
    
    clauses = []
    
    # If the expression is an And, each part is a clause
    if isinstance(expr, And):
        for part in expr.args:
            if isinstance(part, Or):
                # Extract literals from the 'Or' clause
                clauses.append(extract_literals(part))
            else:
                clauses.append([str(part)])
    elif isinstance(expr, Or):
        # Single 'Or' expression, treat as a single clause
        clauses.append(extract_literals(expr))
    else:
        # Single literal (could be positive or negated)
        clauses.append([str(expr)])
    
    return clauses


def resolve(clause1, clause2):
    """Perform resolution between two clauses and return the resolved clause."""
    resolved_clause = []
    clause1_tmp = copy.copy(clause1)
    clause2_tmp = copy.copy(clause2)
    for x in clause1:
        for y in clause2:
            if x == '~' + y or y == '~' + x:
                clause2_tmp.remove(y)
                clause1_tmp.remove(x)
                resolved_clause.append(clause1_tmp + clause2_tmp)
    return resolved_clause

def resolution(belief_base, phi):
    phi = preprocess_equivalent(phi) 
    phi = Not(phi)  # Negate the query
    phi = to_cnf(phi)
    phi_clauses = extract_clauses(phi)
    # print("Query Clauses:", phi_clauses)
    belief_base_clauses = []
    
    for i in range(len(belief_base)):
        belief_base_clauses += extract_clauses(to_cnf(preprocess_equivalent(belief_base[i][0])))
    # print("Knowledge Base Clauses:", belief_base_clauses)
    
    # Combine knowledge base and negated query clauses
    clauses = belief_base_clauses + phi_clauses
    # print("Combined Clauses:", clauses)
    new_clauses = []
    
    while True:   
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                clause1 = clauses[i]
                clause2 = clauses[j]
                resolved_clauses = resolve(clause1, clause2)
                # print("Resolved Clauses:", resolved_clauses)
                for c in resolved_clauses:
                    if not c:
                        return True
                    new_clauses.append(c)
                # print("New Clauses:", new_clauses)
        if all(item in clauses for item in new_clauses):
            return False
        for item in new_clauses:
            if item not in clauses:
                clauses.append(item)
                
if __name__ == "__main__":
    input_str = "r"
    belief_base = [("p", 2), ("p>>q", 1)]

    resolution(belief_base, input_str)


# def add_command(belief_base):
#     print("add_command yet to be implemented")

# def print_belief_base(belief_base):
#     print("--------------------------------------")
#     print("Belief base:")
#     if not belief_base:
#         print("EMPTY")
#     else:
#         for b in belief_base:
#             print(b)
#     print("--------------------------------------")

# def clear_command():
#     return []

# def entails_command(belief_base):
#     print("entails_command yet to be implemented")

# # boolean is false if command is 'q' and the agent should be quit, true otherwise
# def process_input(belief_base):
#     valid_commands = ['a', 'b', 'e', 'c', 'q']
#     command = input("Input command: ")
#     print("""======================================
# COMMAND RESULT:""")
#     if command not in valid_commands:
#         print("INVALID COMMAND")
#     if command == 'a':
#         belief_base = add_command(belief_base)
#     elif command == 'b':
#         print_belief_base(belief_base)
#     elif command == 'c':
#         belief_base = clear_command()
#     elif command == 'e':
#         belief_base = entails_command(belief_base)
#     elif command == 'q':
#         return False, belief_base
#     print("======================================")
#     return True, belief_base

# def main():
#     # agent loop
#     belief_base = []
#     agent_running = True
#     while agent_running:
#         print("""
# --------------------------------------
# belief revision agent
# --------------------------------------
# commands:
# - `a`: add a statement to the belief base
# - `b`: print belief base
# - `c`: clear and item from the belief base
# - `e`: enter a statement to check if it is entailed by the belief base
# - `q`: quit the agent
# --------------------------------------
#               """)

#         agent_running, belief_base = process_input(belief_base)

# if __name__ == "__main__":
#     main()


>>>>>>> f8d9f54 (initial commit)
