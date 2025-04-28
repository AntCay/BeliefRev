from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic.boolalg import And, Not, Implies
from sympy.logic.inference import satisfiable


class Agent:
    KB_parsed = []
    KB_strs = []
    symbols = {}

    def add_command(self):
        inp = input("Formula to add to knowledge base: ")
        for c in inp:
            if ord(c) >= ord('A') and ord(c) <= ord('Z'):
                if c not in self.symbols.keys():
                    self.symbols[c] = symbols(c)
        self.KB_strs.append(inp)
        self.parse_KB()

    def parse_KB(self):
        self.KB = [parse_expr(s, self.symbols) for s in self.KB_strs]

    def print_belief_base(self):
        print("--------------------------------------")
        print("Belief base:")
        if not self.KB_strs:
            print("EMPTY")
        else:
            for b in self.KB_strs:
                print(b)
        print("--------------------------------------")

    def clear_command(self):
        self.symbols = {}
        self.KB_strs = []
        self.KB_parsed = []

    def entails_command(self):
        inp = input("Enter formula to check for entailment: ")
        for c in inp:
            if ord(c) >= ord('A') and ord(c) <= ord('Z'):
                if c not in self.symbols.keys():
                    self.symbols[c] = symbols(c)
        KB_entailment = And(*self.KB_parsed, Not(parse_expr(inp)))
        [print(kb) for kb in self.KB_parsed]
        print("KB entails " + inp) if not satisfiable(KB_entailment) else print("KB does entail " + inp)

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

if __name__ == "__main__":
    agent = Agent()
    agent.main()
