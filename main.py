class Agent:
    def add_command(self, belief_base):
        print("add_command yet to be implemented")

    def print_belief_base(self, belief_base):
        print("--------------------------------------")
        print("Belief base:")
        if not belief_base:
            print("EMPTY")
        else:
            for b in belief_base:
                print(b)
        print("--------------------------------------")

    def clear_command(self):
        return []

    def entails_command(self, belief_base):
        print("entails_command yet to be implemented")

    # boolean is false if command is 'q' and the agent should be quit, true otherwise
    def process_input(self, belief_base):
        valid_commands = ['a', 'b', 'e', 'c', 'q']
        command = input("Input command: ")
        print("""======================================
COMMAND RESULT:""")
        if command not in valid_commands:
            print("INVALID COMMAND")
        if command == 'a':
            belief_base = self.add_command(belief_base)
        elif command == 'b':
            self.print_belief_base(belief_base)
        elif command == 'c':
            belief_base = self.clear_command()
        elif command == 'e':
            belief_base = self.entails_command(belief_base)
        elif command == 'q':
            return False, belief_base
        print("======================================")
        return True, belief_base

    def main(self):
        # agent loop
        belief_base = []
        agent_running = True
        while agent_running:
            print("""
--------------------------------------
belief revision agent
--------------------------------------
commands:
- `a`: add a statement to the belief base
- `b`: print belief base
- `c`: clear and item from the belief base
- `e`: enter a statement to check if it is entailed by the belief base
- `q`: quit the agent
--------------------------------------
                  """)

            agent_running, belief_base = self.process_input(belief_base)

if __name__ == "__main__":
    agent = Agent()
    agent.main()
