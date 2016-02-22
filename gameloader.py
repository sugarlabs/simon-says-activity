
from random import randint

class GameLoader:

    def __init__(self):
        self.buttons = ["Red","Green","Yellow","Blue"]
        self.max_length = 1
        self.current = 0
        self.score = 0
        self.sequence = []
        for i in range(0, self.max_length):
            self.sequence.append(self.buttons[randint(0,3)])

    def get_sequence_list(self):
        return self.sequence

    def get_current_button(self):
        return self.sequence[self.current]

    def go_to_next_button(self):
        self.current += 1
        self.score += 10

    def sequence_end(self):
        if self.current == len(self.sequence):
            return True
        else:
            return False

    def next_level(self):
        self.max_length += 1
        self.current = 0
        self.sequence.append(self.buttons[randint(0,3)])

    def reset_game(self):
        self.max_length = 1
        self.current = 0
        self.score = 0
        self.sequence = []
        for i in range(0, self.max_length):
            self.sequence.append(self.buttons[randint(0,3)])
       
    def get_score(self):
        return self.score
