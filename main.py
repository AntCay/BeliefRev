def add_command():
    print("add_command yet to be implemented")

def clear_command():
    print("clear_command yet to be implemented")

def entails_command():
    print("entails_command yet to be implemented")

# return false if command is quit, true otherwise
def get_input() -> bool:
    valid_commands = ['a', 'e', 'c', 'q']
    command = input("Input command: ")
    print("""======================================
COMMAND RESULT:""")
    if command not in valid_commands:
        print("INVALID COMMAND")
    if command == 'a':
        add_command()
    elif command == 'c':
        clear_command()
    elif command == 'e':
        entails_command()
    elif command == 'q':
        return False
    print("======================================")
    return True

def main():
    # agent loop
    agent_running = True
    while agent_running:
        print("""
--------------------------------------
belief revision agent
--------------------------------------
commands:
- `a`: add a statement to the belief base
- `c`: clear and item from the belief base
- `e`: enter a statement to check if it is entailed by the belief base
- `q`: quit the agent
--------------------------------------
              """)
        agent_running = get_input()

if __name__ == "__main__":
    main()

