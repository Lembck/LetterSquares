import json

data = None
with open("fourletters.json", "r") as f:
    data = json.load(f)

grid = []

for i in range(4):
    grid.append([])
    for j in range(4):
        x = set(data[str(i)].keys()).intersection(set(data[str(j)].keys()))
        grid[i].append(x)

def combine(row):
    first, second, third, fourth = row
    combined = set()
    for a in first:
        for b in second:
            for c in third:
                for d in fourth:
                    try:
                        word_count = len(data["0"][a]["1"][b]["2"][c]["3"][d])
                        combined.add(a + b + c + d)
                    except:
                        continue
    return combined

w = combine(grid[0])

x = combine(grid[1])

y = combine(grid[2])

z = combine(grid[3])

def first_two(first, second):
    total = len(first)
    so_far = 0
    works = set()
    for A in first:
        if so_far % int(total / 10) == 0:
            print("first_two", so_far, total)
        so_far += 1
        for B in second:
            try:
                word_count = len(data["0"][A[0]]["1"][B[0]])
                word_count = len(data["0"][A[1]]["1"][B[1]])
                word_count = len(data["0"][A[2]]["1"][B[2]])
                word_count = len(data["0"][A[3]]["1"][B[3]])
                word_count = len(data["0"][A[0]]["1"][B[1]])
                word_count = len(data["0"][A[3]]["1"][B[2]])
                works.add((A, B))
            except:
                continue
    return works

def next_one(first_two, third):
    total = len(first_two)
    so_far = 0
    works = set()
    for AB in first_two:
        A, B = AB
        if so_far % int(total / 10) == 0:
            print("next_one", so_far, total)
        so_far += 1
        for C in third:
            try:
                word_count = len(data["0"][A[0]]["1"][B[0]]["2"][C[0]])
                word_count = len(data["0"][A[1]]["1"][B[1]]["2"][C[1]])
                word_count = len(data["0"][A[2]]["1"][B[2]]["2"][C[2]])
                word_count = len(data["0"][A[3]]["1"][B[3]]["2"][C[3]])
                word_count = len(data["0"][A[0]]["1"][B[1]]["2"][C[2]])
                word_count = len(data["0"][A[3]]["1"][B[2]]["2"][C[1]])
                works.add((A, B, C))
            except:
                continue
    return works
I = first_two(w, x)
J = next_one(I, y)

def form(first, second, third, fourth):
    total = len(first)
    so_far = 0
    works = set()
    for A in first:
        if so_far % int(total / 10) == 0:
            print(so_far, total)
        so_far += 1
        for B in second:
            for C in third:
                for D in fourth:
                    try:
                        word_count = len(data["0"][A[0]]["1"][B[0]]["2"][C[0]]["3"][D[0]])
                        word_count = len(data["0"][A[1]]["1"][B[1]]["2"][C[1]]["3"][D[1]])
                        word_count = len(data["0"][A[2]]["1"][B[2]]["2"][C[2]]["3"][D[2]])
                        word_count = len(data["0"][A[3]]["1"][B[3]]["2"][C[3]]["3"][D[3]])
                        word_count = len(data["0"][A[0]]["1"][B[1]]["2"][C[2]]["3"][D[3]])
                        word_count = len(data["0"][A[3]]["1"][B[2]]["2"][C[1]]["3"][D[0]])
                        print("adding", A, B, C, D)
                        works.add((A, B, C, D))
                    except:
                        continue
    return works

#answer = form(x, y, z)
