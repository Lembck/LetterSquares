import re
import random
import copy
from functools import reduce

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
        if True or self.grid[x][y] != letter:
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

    def order_to_fill(self):
        enumerated = list(enumerate(zip(self.possibilities, self.spots_complete)))
        enumerated.sort(key=lambda x: x[1][0])
        enumerated = [index for index, y in enumerated if not y[1]]

        #bias to fill diagonals first
        if 8 in enumerated and 9 in enumerated:
            eight_index = enumerated.index(8)
            nine_index = enumerated.index(9)
            if eight_index <= nine_index:
                enumerated.pop(nine_index)
                enumerated.pop(eight_index)
                enumerated = [8, 9] + enumerated
            if eight_index > nine_index:
                enumerated.pop(eight_index)
                enumerated.pop(nine_index)
                enumerated = [9, 8] + enumerated
        elif 8 in enumerated:
            eight_index = enumerated.index(8)
            enumerated.pop(eight_index)
            enumerated = [8] + enumerated
        elif 9 in enumerated:
            nine_index = enumerated.index(9)
            enumerated.pop(nine_index)
            enumerated = [9] + enumerated
            
        return enumerated

    def undo(self):
        index, last_move = self.history.pop()
        self.spots_complete[index] = False
        for package in last_move:
            if package:
                self.grid[package[0]][package[1]] = "."
        self.set_possibilities()

    def sorted_words(self, index):
        all_words = []
        for word in words:
            self.add_word_in_spot(word, index)
            self.set_possibilities()
            score = sum(self.possibilities)
            all_words.append((word, score))
        all_words.sort(key=lambda x: x[1], reverse=True)
        print(all_words)
        return map(lambda x: x[0], all_words)


    def alternate_approach(self):
        best = (words[0], words[0], 0)
        eight_words = list(self.sorted_words(8))
        nine_words =  list(self.sorted_words(9))
        all_pairs = []
        for eight_word in eight_words:
            self.add_word_in_spot(eight_word, 8)
            for nine_word in nine_words:
                #print(eight_word, nine_word)
                self.add_word_in_spot(nine_word, 9)
                self.set_possibilities()
                score = reduce(lambda x, y: x * y, self.possibilities)
                all_pairs.append((eight_word, nine_word, score))
                if score > best[2]:
                    best = (eight_word, nine_word, score)
                    print("new best", best)
        print(best)
        all_pairs.sort(key=lambda x: x[2], reverse=True)
        return all_pairs

    def start(self):
        self.set_possibilities()
        self.add_word_in_spot("sons", 8)
        self.add_word_in_spot("soot", 9)
        self.step(0, [])

    def add_grid_to_deadends(self):
        if len(self.deadends) % 1000 == 0:
            print("tried:", len(self.deadends))
        self.deadends.append(copy.deepcopy(self.grid))
        
    def step(self, deep, used_words):
        if deep >= self.deepest:
            print(deep, "deep")
            self.print_grid()
            self.deepest = deep

        if self.grid in self.deadends:
            return

        indexes = self.order_to_fill()
        for index in indexes:
            current_word = self.get_words()[index]
            choices = re.findall(r'\b' + current_word.replace(".", "\w"), " ".join(words))
            random.shuffle(choices)
            for choice in choices:
                if choice in used_words:
                    continue
                self.add_word_in_spot(choice, index)
                if self.grid in self.deadends:
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
<<<<<<< HEAD
x = s.alternate_approach()
=======
s.start()
>>>>>>> 56fbf3c7aa971e0763868f5f38775c5ff9cd73ff
