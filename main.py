from agent import Agent
from mastermind import Mastermind
import numpy as np
import matplotlib.pyplot as plt


def play_mastermind():
    final_turn_count_list = []
    for game in range(100):
        # initialise
        mastermind = Mastermind()
        code_breaker = Agent()
        init_guess = "y_1&p_2&m_3&b_4"

        code_breaker.expand_command(mastermind.init_state)
        #code_breaker.print_belief_base()

        feedback = mastermind.guess_state(init_guess)
        if isinstance(feedback, str):
            #print(feedback)
            code_breaker.revise_command(feedback)
            #code_breaker.print_belief_base()
        else:
            print("Game won in " + str(feedback) + " turns!")
            final_turn_count_list.append(feedback)

        while not mastermind.game_over:
            guess = mastermind.generate_guess(code_breaker)
            #print("Turn count: ", mastermind.guess_count)
            #print("Guess: " + guess)
            feedback = mastermind.guess_state(guess)
            if isinstance(feedback, str):
                #print("Feedback: " + feedback)
                code_breaker.revise_command(feedback)
                #code_breaker.print_belief_base()
            else:
                print("Game won in " + str(feedback) + " turns!")
                final_turn_count_list.append(feedback)
    final_turn_count_array = np.array(final_turn_count_list)
    plt.hist(final_turn_count_array, bins = 7,density=True, color = 'blue', edgecolor = 'black')
    plt.xlabel('Winning turn')
    plt.ylabel('Frequency')
    plt.savefig('mastermind.png')
    plt.show()

if __name__ == "__main__":
    play_mastermind()
    #agent = Agent()
    #agent.main()

