from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import And, Not, Implies
from sympy.logic.inference import satisfiable
from sympy import symbols

vars = "ABC"
s = {}
for c in vars:
    s[c] = symbols(c)

a = parse_expr("A", s)
b = parse_expr("~A", s)
print(satisfiable(And(a, b)))

