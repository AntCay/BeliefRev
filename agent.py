from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import And, Not, Implies
from sympy.logic.inference import satisfiable
from logic import *
from revision import *

class Agent:
    kb_num = 0
    KB_strs = []
    symbols = {}

    def expand_command(self, inp):
        expansion(self, inp)
        # self.KB_strs.append((inp, self.kb_num))
        # self.kb_num += 1

    def print_belief_base(self):
        print("--------------------------------------")
        print("Belief base:")
        if not self.KB_strs:
            print("EMPTY")
        else:
            for b in self.KB_strs:
                print(str(b[1]) + ". " + b[0])
        print("--------------------------------------")

    def contract_command(self, inp):
        contract(self, str(Not(inp)))

    def revise_command(self, inp):
        revise(self, inp)

    def clear_command(self):
        self.symbols = {}
        self.KB_strs = []
        self.kb_num = 0

    def entails_command(self, inp):
        print("Entails: " + str(entailment(self.KB_strs, inp)))

    # boolean is false if command is 'q' and the agent should be quit, true otherwise
    def process_input(self):
        valid_commands = ['a', 'b', 'd', 'r', 'e', 'c', 'q']
        command = input("Input command: ")
        if command not in valid_commands:
            print("INVALID COMMAND")
        if command == 'a':
            inp = input("Formula to add to knowledge base: ")
            print("""======================================
COMMAND RESULT:""")
            self.expand_command(inp)
        elif command == 'b':
            self.print_belief_base()
        elif command == 'c':
            self.clear_command()
        elif command == 'd':
            inp = input("Enter belief to contract from belief base: ")
            print("""======================================
COMMAND RESULT:""")
            self.contract_command(inp)
        elif command == 'e':
            inp = input("Fomula to check for entailment: ")
            print("""======================================
COMMAND RESULT:""")
            self.entails_command(inp)
        elif command == 'r':
            inp = input("Enter belief to revise with belief base: ")
            print("""======================================
COMMAND RESULT:""")
            self.revise_command(inp)
        elif command == 'q':
            return False
        print("======================================")
        return True


    def main(self):
        # agent loop
        agent_running = True
        while agent_running:
            print("""
--------------------------------------
belief revision agent
--------------------------------------
commands:
- `a`: add a statement to the belief base (expansion)
- `b`: print belief base
- `c`: clear the belief base
- `d`: delete a statement from the belief base (contraction)
- `e`: enter a statement to check if it is entailed by the belief base
- `q`: quit the agent
- `r`: revise the belief base with the following statement (revision)
--------------------------------------
                  """)

            agent_running = self.process_input()
            self.print_belief_base()
