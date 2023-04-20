import json

data = None
with open("threeletters.json", "r") as f:
    data = json.load(f)


words = None
with open("threeletters.txt", "r") as f:
    words = [line.strip() for line in f.readlines()]


a_possibilities = set(data["0"].keys())
b_possibilities = set(data["0"].keys()).intersection(set(data["1"].keys()))
c_possibilities = set(data["0"].keys()).intersection(set(data["2"].keys()))
d_possibilities = set(data["0"].keys()).intersection(set(data["1"].keys()))
e_possibilities = set(data["1"].keys())
f_possibilities = set(data["1"].keys()).intersection(set(data["2"].keys()))
g_possibilities = set(data["0"].keys()).intersection(set(data["2"].keys()))
h_possibilities = set(data["1"].keys()).intersection(set(data["2"].keys()))
i_possibilities = set(data["2"].keys())

def combine(first, second, third):
    combined = set()
    for a in first:
        for b in second:
            for c in third:
                try:
                    word_count = len(data["0"][a]["1"][b]["2"][c])
                    combined.add(a + b + c)
                except:
                    continue
    return combined

x = combine(a_possibilities, b_possibilities, c_possibilities)

y = combine(d_possibilities, e_possibilities, f_possibilities)

z = combine(g_possibilities, h_possibilities, i_possibilities)

def form(first, second, third):
    total = len(first)
    so_far = 0
    works = set()
    for A in first:
        if so_far % int(total / 10) == 0:
            print(so_far, total)
        so_far += 1
        for B in second:
            for C in third:
                try:
                    word_count = len(data["0"][A[0]]["1"][B[0]]["2"][C[0]])
                    word_count = len(data["0"][A[1]]["1"][B[1]]["2"][C[1]])
                    word_count = len(data["0"][A[2]]["1"][B[2]]["2"][C[2]])
                    word_count = len(data["0"][A[0]]["1"][B[1]]["2"][C[2]])
                    word_count = len(data["0"][A[2]]["1"][B[1]]["2"][C[0]])
                    print("adding", A, B, C)
                    works.add((A, B, C))
                except:
                    continue
    return works

answer = form(x, y, z)
