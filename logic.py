from sympy.logic.boolalg import to_cnf, Or, And, Not
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

# Function to perform resolution between two clauses and return the resolved clause
def resolve(clause1, clause2):
    resolved_clause = []
    clause1_tmp = copy.copy(clause1)
    clause2_tmp = copy.copy(clause2)
    for x in clause1:
        for y in clause2:
            if x == '~' + y or y == '~' + x:
                if y in clause2_tmp: clause2_tmp.remove(y)
                if x in clause1_tmp: clause1_tmp.remove(x)
                resolved_clause.append(clause1_tmp + clause2_tmp)
    return resolved_clause

def resolution(clauses):
    new_clauses = []
    while True:   
        for clause1, clause2 in itertools.combinations(clauses, 2):
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

# function to check belief base entails the query (new belief)                
def entailment(belief_base=[], phi=""):
    phi_clauses = []
    # Negated, convert to CNF and extract clauses from the query
    if not phi == "":
        phi = preprocess_equivalent(phi) 
        phi = Not(phi)  # Negate the query
        phi = to_cnf(phi)
        phi_clauses = extract_clauses(phi)
    
    belief_base_clauses = []
    # Convert each belief base formula to CNF and extract clauses
    for i in range(len(belief_base)):
        belief_base_clauses += extract_clauses(to_cnf(preprocess_equivalent(belief_base[i][0])))

    # Combine belif base and negated query clauses
    clauses = belief_base_clauses + phi_clauses
    
    # perform resolution to check if the negated query is a logical consequence of the belief base
    return resolution(clauses)

# function to check consustency of a set of formulas
def check_consistency(formulas=[], new_formula=""):
    negated_new_formula = str(Not(new_formula))
    
    # if resolution return false means the formulas is consistent
    return not entailment(formulas, negated_new_formula) 
