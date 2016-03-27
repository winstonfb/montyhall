""" Simulate the Monty Hall 'paradox'."""

from scipy.stats import rv_discrete
from fractions import Fraction
import sys


if __name__ == '__main__':

    class Doors:
        """ Assign values to doors and select them as per simulated strategy.

        Attributes:
            values: Boolean indicating whether the door in that position contains a prize.
            probs: A list giving, for each door, the probability that this door will be the one with a prize.
            prize_door: A single randomly chosen discrete value from a probability distribution over discrete values;
             the door in this position has the prize.
            choice_first: A single randomly chosen discrete value from probability distribution over discrete values;
             this represents the player's first choice.
            goat_door: A single randomly chosen discrete value from probability distribution over discrete values;
             the door in this position is opened to reveal a goat. Which is not a prize.
            selection: A list of valid door selections for the host to open.
            choice_second: The player's final choice of doors, contingent on strategy
             (0 -> stay with first choice. 1 -> switch to unopened door.)

        Note:
            Some attributes (selection, choice_second, goat_door) assigned values 
            in class methods for the sake of illustration.

        """
        
        def __init__(self):
            self.values = [0, 0, 0]
            self.probs = [Fraction(1, 3)]*3

            self.prize_door = rv_discrete(name = 'prize_door_selection', values =
                (range(len(self.values)), self.probs
                    )).rvs(size=1)
            self.values[self.prize_door[0]] = 1
            
            self.choice_first = rv_discrete(name = 'first_choice_selection', values =
                (range(len(self.values)), self.probs
                    )).rvs(size=1)

            self.selection = None
            self.choice_second = None
            self.goat_door = None
        
        def reveal_goat(self):
            """ Open one door to reveal a goat (non-prize). 
            Valid doors to open depend on choice_first.
            """

            if self.prize_door[0] == self.choice_first[0]:
                self.probs = [.5]*3
            
            else:
                self.probs = [1]*3

            self.probs[self.prize_door[0]] = 0
            self.probs[self.choice_first[0]] = 0

            self.goat_door = rv_discrete(name = 'goat_door_selection', values=
                (range(len(self.values)), self.probs
                    )).rvs(size=1)
        
        def choose_door(self, strategy):
            """ Choose a door based on player strategy (stay or switch). 
            
            Args:
                strategy: 1 to switch to new, unopened door; 0 to stay with first choice.

            """
            if strategy == 0:
                self.choice_second = self.choice_first
            
            else:
                self.selection = [0, 1, 2]
                self.selection.remove(self.choice_first[0])
                self.selection.remove(self.goat_door[0])
                self.choice_second = self.selection[0]

        def tally_score(self):
            """ Return a score for the trial.

            Returns:
                1 if the chosen door has a prize; 0 otherwise.

            """
            if self.choice_second == self.prize_door:
                return 1
            else:
                return 0


    try:
        TRIALS = int(sys.argv[1])
    except (IndexError, ValueError):
        TRIALS = 1000

    for y in range(0, 2):
        total_score = 0
        for x in range(1, TRIALS):
            test = Doors()
            test.reveal_goat()
            test.choose_door(strategy=y)
            trial_score = test.tally_score()
            total_score += trial_score
        win_percentage = '{0:.2f}'.format((float(total_score) / float(TRIALS)) * 100)
        if y == 1: 
            print("Strategy: switch doors | Trials: {0} | Wins: {1} ({2}%)".format(TRIALS, total_score, win_percentage))
        else:
            print("Strategy: don\'t switch | Trials: {0} | Wins: {1} ({2}%)".format(TRIALS, total_score, win_percentage))