import json

data = None
#with open("threeletters.json", "r+") as f:
#    data = json.load(f)

def writeData(data):
    with open("fourletters.json", "w") as f:
        #f.seek(0) # reset file position to the beginning.
        json.dump(data, f, indent=4)
        #f.truncate() # remove remaining part

words = []

with open("fourletters.txt", "r") as f:
    # words = f.readline().split("") read file with spaces
    for line in f:
        words.append(line.strip())

def preComputeLetter(charsAtIndex, char, i, word):
    try:
        charsAtIndex[i][str(char)][words] += [word]
    except:
        charAtIndex = dict()
        try:
            charAtIndex = charsAtIndex[i]
        except:
            charAtIndex = dict()
        try:
            charAtIndex[str(char)]["words"] += [word]
        except:
            charAtIndex[str(char)] = dict()
            charAtIndex[str(char)]["words"] = [word]
        charsAtIndex[i] = charAtIndex
    

def preComputeWord(charsAtIndex, originalWord, word, indexes):
    for i, char in zip(indexes, word):
        preComputeLetter(charsAtIndex, char, i, originalWord)
        wordWithoutOneChar = list(word)
        wordWithoutOneChar.remove(char)
        wordWithoutOneChar = "".join(wordWithoutOneChar)
        remainingIndexes = indexes.copy()
        remainingIndexes.remove(i)
        if len(remainingIndexes) > 0:
            preComputeWord(charsAtIndex[i][str(char)], originalWord, wordWithoutOneChar, remainingIndexes)
        # for j, char2 in zip(remainingIndexes, wordWithoutOneChar):
        #     preComputeLetter(charsAtIndex[i][str(char)], char2, j, word)
        #     wordWithoutTwoChars = wordWithoutOneChar[:j] + wordWithoutOneChar[j+1:]
        #     remainingIndexes2 = remainingIndexes.copy()
        #     remainingIndexes2.remove(j)
        #     for k, char3 in zip(remainingIndexes2, wordWithoutTwoChars):
        #         preComputeLetter(charsAtIndex[i][str(char)][j][str(char2)], char3, k, word)
        #         wordWithoutFourChars = wordWithoutTwoChars[:k] + wordWithoutTwoChars[k+1:]
        #         remainingIndexes3 = remainingIndexes2.copy()
        #         remainingIndexes3.remove(k)
        #         for l, char4 in zip(remainingIndexes3, wordWithoutFourChars):
        #             preComputeLetter(charsAtIndex[i][str(char)][j][str(char2)][k][str(char3)], char4, l, word)
    

def preCompute():
    data = dict()
    for word in words:
        indexes = [0, 1, 2, 3]
        preComputeWord(data, word, word, indexes)
    print(data)
    with open("fourletters.json", "w") as f:
        #f.seek(0) # reset file position to the beginning.
        json.dump(data, f, indent=4)

preCompute()

