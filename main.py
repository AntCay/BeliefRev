from agent import Agent
from mastermind import Mastermind


def play_mastermind():
    # initialise
    mastermind = Mastermind()
    code_breaker = Agent()
    init_guess = "y_1&p_2&m_3&b_4"

    code_breaker.expand_command(mastermind.init_state)
    code_breaker.print_belief_base()

    feedback = mastermind.guess_state(init_guess)
    if isinstance(feedback, str):
        print(feedback)
        code_breaker.revise_command(feedback)
        # code_breaker.print_belief_base()
    else:
        print("Game won in " + str(feedback) + " turns!")

    while not mastermind.game_over and mastermind.guess_count < 8:
        guess = mastermind.generate_guess(code_breaker)
        print("Guess: " + guess)
        feedback = mastermind.guess_state(guess)
        if isinstance(feedback, str):
            print("Feedback: " + feedback)
            code_breaker.revise_command(feedback)
            # code_breaker.print_belief_base()
        else:
            print("Game won in " + str(feedback) + " turns!")
    else:
        print("Game lost in " + str(mastermind.guess_count) + " turns!")


if __name__ == "__main__":
    play_mastermind()
    #agent = Agent()
    #agent.main()
