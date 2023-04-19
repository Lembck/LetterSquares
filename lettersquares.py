import re
import random
import copy

vowels = "aeiouy"

dictionary = {}
words = []

def add_template(word):
    
    combination = ""
    for letter in word:
        if letter in vowels:
            combination = combination + "v"
        else:
            combination = combination + "c"
    
    try:
        dictionary[combination] += 1
    except:
        dictionary[combination] = 1

with open("fourletters.txt", "r") as f:
    # words = f.readline().split("") read file with spaces
    words = []
    for line in f:
        words.append(line.strip())
    #for word in words:
    #    add_template(word)

#print(sorted(dictionary.items(), key=lambda x:x[1], reverse=True))

#def valid_board():
SIZE = 4

def wait():
    if input() == '':
        return True
   
class Square:
    def __init__(self):
        self.grid = [[".", ".", ".", "."],
                     [".", ".", ".", "."],
                     [".", ".", ".", "."],
                     [".", ".", ".", "."]]
        self.spots_complete = [False, False, False, False, False,
                               False, False, False, False, False]
        self.possibilities = [False, False, False, False, False,
                               False, False, False, False, False]
        self.history = []
        self.deepest = -1
        self.deadends = []

    def flipped_grid(self):
        return list(zip(*self.grid))

    def print_grid(self):
        print("\n".join(["".join(row) for row in self.grid]))

    def horizontal_words(self):
        words = []
        for row in range(SIZE):
            words.append("".join(self.grid[row]))
        return words

    def vertical_words(self):
        words = []
        for col in range(SIZE):
            words.append("".join(self.flipped_grid()[col]))
        return words

    def diagonal_words(self):
        right = ""
        for i in range(SIZE):
            right += self.grid[i][i]
        left = ""
        for i in range(len(self.grid)):
            left += self.grid[SIZE-1-i][i]
        return [right, left]

    def get_words(self):
        return self.horizontal_words() + self.vertical_words() + self.diagonal_words()

    def add_letter_in_spot(self, x, y, letter):
        if self.grid[x][y] != letter:
            self.grid[x][y] = letter
            return [x, y, letter]

    def add_word_in_spot(self, word, spot):
        #print("in add_word_in_spot 1")
        changes = []
        if spot < SIZE:
            for i in range(SIZE):
                changes.append(self.add_letter_in_spot(spot, i, word[i]))
        elif spot < SIZE * 2:
            for i in range(SIZE):
                changes.append(self.add_letter_in_spot(i, spot-SIZE, word[i]))
        elif spot == 8:
            for i in range(SIZE):
                changes.append(self.add_letter_in_spot(i, i, word[i]))
        elif spot == 9:
            for i in range(SIZE):
                changes.append(self.add_letter_in_spot(SIZE-1-i, i, word[i]))
        else:
            return
        #print("in add_word_in_spot 2")
        self.spots_complete[spot] = True
        #print(changes)
        #print(self.spots_complete)
        self.history.append((spot, changes))        

    def set_possibilities(self):
        for i, word in enumerate(self.get_words()):
            row = "".join(word).replace(".", "\w")
            #print(row)
            result = re.findall(r'\b' + row, " ".join(words))
            self.possibilities[i] = len(result)

    def its_fucked(self):
        if min(self.possibilities) == 0:
            return True
        return False

    def least_not_filled(self):
        enumerated = list(enumerate(zip(self.possibilities, self.spots_complete)))
        enumerated.sort(key=lambda x: x[1][0])
        enumerated = [index for index, y in enumerated if not y[1]]
        #print(enumerated)
        return enumerated

    def undo(self):
        index, last_move = self.history.pop()
        self.spots_complete[index] = False
        for package in last_move:
            if package:
                self.grid[package[0]][package[1]] = "."
        self.set_possibilities()

    def start(self):
        #word = words[0] #get a word
        #self.add_word_in_spot(word, 1) #add it somewhere (to the diagonal)
        #self.add_word_in_spot("ashy", 0)
        #self.add_word_in_spot("huhs", 6)
        #self.print_grid()
        self.set_possibilities()
        self.step(0, [])
##        self.add_word_in_spot("yaks", 7)
##        self.print_grid()
##        print(self.possibilities)
##        index = self.least_not_filled()
##        current_word = self.get_words()[index]
##        choices = re.findall(r'\b' + current_word.replace(".", "\w"), " ".join(words))
##        print(index, choices)

    def add_grid_to_deadends(self):
        if len(self.deadends) % 100 == 0:
            print("adding:", len(self.deadends))
        if self.grid in self.deadends:
            print("dupe")
        else:
            self.deadends.append(copy.deepcopy(self.grid))
        
    def step(self, deep, used_words):
        if deep >= self.deepest:
            print(deep, "deep")
            self.print_grid()
            self.deepest = deep

        if self.grid in self.deadends:
            return

        indexes = self.least_not_filled()
        for index in indexes:
            current_word = self.get_words()[index]
            choices = re.findall(r'\b' + current_word.replace(".", "\w"), " ".join(words))
            random.shuffle(choices)
            for choice in choices:
                if choice in used_words:
                    continue
                self.add_word_in_spot(choice, index)
                if self.grid in self.deadends:
                    print("180")
                    self.undo()
                    continue
                self.set_possibilities()
                if self.its_fucked():
                    self.add_grid_to_deadends()
                    self.undo()
                else:
                    if self.step(deep + 1, used_words + [choice]):
                        return True
        
        if all(self.spots_complete):
            return True
        self.add_grid_to_deadends()
        self.undo()      
            
        #print(current_word)
        
        #print(choices)
        #get the minimum of the possibilities where the row isn't full
        #repeat the process with that
        #stop if you get to zero
        #need to keep a log so you can undo.

    
        

s = Square()
s.start()
