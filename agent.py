from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import And, Not, Implies
from sympy.logic.inference import satisfiable
from logic import *

class Agent:
    kb_num = 0
    KB_strs = []
    symbols = {}

    def add_command(self):
        inp = input("Formula to add to knowledge base: ")
        self.KB_strs.append((inp, self.kb_num))
        self.kb_num += 1

    def print_belief_base(self):
        print("--------------------------------------")
        print("Belief base:")
        if not self.KB_strs:
            print("EMPTY")
        else:
            for b in self.KB_strs:
                print(str(b[1]) + ". " + b[0])
        print("--------------------------------------")

    def clear_command(self):
        self.symbols = {}
        self.KB_strs = []
        self.kb_num = 0

    def entails_command(self):
        inp = input("Fomula to check for entailment: ")
        print("entails: " + str(resolution(self.KB_strs, inp)))

    # boolean is false if command is 'q' and the agent should be quit, true otherwise
    def process_input(self):
        valid_commands = ['a', 'b', 'e', 'c', 'q']
        command = input("Input command: ")
        print("""======================================
COMMAND RESULT:""")
        if command not in valid_commands:
            print("INVALID COMMAND")
        if command == 'a':
            self.add_command()
        elif command == 'b':
            self.print_belief_base()
        elif command == 'c':
            self.clear_command()
        elif command == 'e':
            self.entails_command()
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
- `a`: add a statement to the belief base
- `b`: print belief base
- `c`: clear the belief base
- `e`: enter a statement to check if it is entailed by the belief base
- `q`: quit the agent
--------------------------------------
                  """)

            agent_running = self.process_input()
