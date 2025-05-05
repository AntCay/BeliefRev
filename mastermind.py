from sympy.logic.boolalg import to_cnf
import random
from logic import extract_clauses, resolve, resolution
from agent import Agent

class Mastermind:
    def __init__(self):
        self.guess_count = 0
        self.game_over = False
        self.colours = "rbgopbwmy"
        self.spots = ("_1", "_2", "_3", "_4")
        self.init_state = ""
        self.goal_state = ""

        for spot in self.spots:
            self.init_state += '('
            for colour in self.colours:
                self.init_state += colour + spot + '|'
            self.init_state = self.init_state[:-1] + ')' + '&'
        self.init_state = self.init_state[:-1]

        for spot in self.spots:
            self.goal_state += random.choice(self.colours) + spot + '&'
        self.goal_state = self.goal_state[:-1]
        self.cnf_goal = to_cnf(self.goal_state)
        # Extracting goal letters from the cnf for later
        self.goal_colours = "".join([extract_clauses(self.cnf_goal)[i][0][0] for i in range(4)])


    def guess_state(self, guess):
        self.guess_count += 1
        guess = to_cnf(guess)
        # Check if guess is goal state
        if guess == self.cnf_goal:
            self.game_over = True
            return self.guess_count
        guess = extract_clauses(guess)
        goal_state = extract_clauses(self.cnf_goal)

        # Sort guess by spot and answer by spot
        guess.sort(key=lambda e : [e[x][2] for x in range(len(e))])
        goal_state.sort(key=lambda e : [e[x][2] for x in range(len(e))])
        feedback = ""

        for i, entry in enumerate(guess):
            # Generate exact matches
            if entry == goal_state[i]:
                feedback += "".join(entry) + '&'
            else:
                if not any(entry[0][0] == x for x in self.goal_colours):
                    feedback += '('
                    for spot in self.spots:
                        feedback += '~' + "".join(entry[0][0]) + spot + '&'
                    feedback = feedback[:-1] + ')' + '&'
                else:
                    feedback += '~' + str(entry[0]) + '&'
        feedback = feedback[:-1]
        return feedback

    @staticmethod
    def generate_guess(code_breaker):
        guess = ""
        for k in range(1,5):
            for belief, _ in code_breaker.KB_strs:
                extracted_belief = extract_clauses(to_cnf(belief))[0]
                if extracted_belief [0][0] != '~' and extracted_belief [0][2] == str(k):
                    guess += random.choice(extracted_belief) + "&"
                    break
        guess = guess[:-1]
        return guess

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
        code_breaker.print_belief_base()
    else:
        print("Game won in " + str(feedback) + " turns!")

    while not mastermind.game_over:
        guess = mastermind.generate_guess(code_breaker)
        print("Turn count: ", mastermind.guess_count)
        print("Guess: " + guess)
        feedback = mastermind.guess_state(guess)
        if isinstance(feedback, str):
            print("Feedback: " + feedback)
            code_breaker.revise_command(feedback)
            code_breaker.print_belief_base()
        else:
            print("Game won in " + str(feedback) + " turns!")

if __name__ == "__main__":
    play_mastermind()
