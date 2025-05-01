from sympy.logic.boolalg import to_cnf
import random
from logic import extract_clauses

class Mastermind:
    def __init__(self):
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
        guess = to_cnf(guess)
        # Check if guess is goal state
        if guess == self.cnf_goal:
            return True
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

game = Mastermind()
print(game.init_state)
print(game.goal_state)
print(game.guess_state("y_1&p_2&m_3&b_4"))
