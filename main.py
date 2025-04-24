def add_command(belief_base):
    print("add_command yet to be implemented")

def print_belief_base(belief_base):
    print("--------------------------------------")
    print("Belief base:")
    if not belief_base:
        print("EMPTY")
    else:
        for b in belief_base:
            print(b)
    print("--------------------------------------")

def clear_command():
    return []

def entails_command(belief_base):
    print("entails_command yet to be implemented")

# boolean is false if command is 'q' and the agent should be quit, true otherwise
def process_input(belief_base):
    valid_commands = ['a', 'b', 'e', 'c', 'q']
    command = input("Input command: ")
    print("""======================================
COMMAND RESULT:""")
    if command not in valid_commands:
        print("INVALID COMMAND")
    if command == 'a':
        belief_base = add_command(belief_base)
    elif command == 'b':
        print_belief_base(belief_base)
    elif command == 'c':
        belief_base = clear_command()
    elif command == 'e':
        belief_base = entails_command(belief_base)
    elif command == 'q':
        return False, belief_base
    print("======================================")
    return True, belief_base

def main():
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

        agent_running, belief_base = process_input(belief_base)

if __name__ == "__main__":
    main()
