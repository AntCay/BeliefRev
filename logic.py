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
    input_str = "~r"
    belief_base = [("p", 2), ("p&q&r", 1)]

    print(resolution(belief_base, input_str))
