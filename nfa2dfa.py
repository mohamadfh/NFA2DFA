import pprint

# getting inputs and giving them proper structure

nmsq = list(map(lambda x: int(x), input().split()))
finalstatesbinary = list(map(lambda x: int(x), input().split()))
startstates = input().split()
transitions = {}
alphabets = []
finalstates = []

for i in range(len(finalstatesbinary)):
    if finalstatesbinary[i]:
        finalstates.append(str(i+1))

for i in range(nmsq[1]):

    transition = input().split()
    if transition[0] not in alphabets and transition[0] != "-":
        alphabets.append(transition[0])
    if transition[1] in transitions.keys():
        if transition[0] in transitions[transition[1]].keys():
            transitions[transition[1]][transition[0]].append(transition[2])
        else:
            transitions[transition[1]][transition[0]] = [transition[2]]
    else:

        transitions[transition[1]] = {transition[0]: [transition[2]]}

inputstrings = []

for i in range(nmsq[3]):
    inp = input()
    inputstrings.append(inp)
alphabets = sorted(alphabets)

# defining nfa and dfa classes

class DFA:
    def __init__(self, states, alphabets, startstate, finalstates, transitions):
        self.states = states
        self.transitions = transitions
        self.finalstates = finalstates
        self.startstate = startstate
        self.alphabets = alphabets

    def accept(self,string):
        currentstate = self.startstate
        statepath = []
        string = string.replace("-","")
        for letter in string:
            currentstate = self.transitions[currentstate][letter]
            statepath.append(currentstate)
        return currentstate in self.finalstates, statepath

class NFA:
    def __init__(self, states, alphabets, startstates, finalstates, transitions):
        self.states = states
        self.transitions = transitions
        self.finalstates = finalstates
        self.startstates = startstates
        self.alphabets = alphabets

    def epsilonclosure(self, state):
        res = [state]
        nextstates = self.transitions[state].get("-", [])
        for nextstate in nextstates:
            res.extend(self.epsilonclosure(nextstate))

        return list(set(res))

    def toDFA(self):
        dfastates = []
        dfatransitions = {}
        dfafinalstates = []
        dfastartstate = set()
        for ss in self.startstates:
            dfastartstate.update(self.epsilonclosure(ss))
        dfastartstate = str.join(' ', sorted(dfastartstate))

        newstates = [dfastartstate]

        while len(newstates) > 0:
            currentstate = newstates.pop()
            isfinal = False
            for alphabet in self.alphabets:
                destinationstate = set()
                for s in currentstate.split():
                    isfinal |= s in self.finalstates
                    s = self.epsilonclosure(s)
                    for m in s:
                        if(alphabet not in self.transitions[m]):
                            continue
                        for t in self.transitions[m][alphabet]:
                            destinationstate.update(self.epsilonclosure(t))
                destinationstate = str.join(' ', sorted(destinationstate))
                if destinationstate not in newstates and destinationstate not in dfastates and currentstate != destinationstate:
                    newstates.append(destinationstate)
                if currentstate not in dfatransitions:
                    dfatransitions[currentstate] = dict()
                dfatransitions[currentstate][alphabet] = destinationstate

            dfastates.append(currentstate)

            if isfinal:
                dfafinalstates.append(currentstate)
        res = DFA(dfastates, self.alphabets, dfastartstate, dfafinalstates, dfatransitions)
        return res


#printing wanted output
inputnfa = NFA(list(map(lambda x: str(x + 1), range(nmsq[0]))), alphabets, startstates, finalstates, transitions)
dfa = inputnfa.toDFA()

changedname = dict()
for i in range(len(dfa.states)):
    changedname[dfa.states[i]] = str(i + 1)

print(len(dfa.states),end=" ")
print(len(dfa.states)*len(dfa.alphabets),end=" ")
print(changedname[dfa.startstate])
for s in dfa.states:
    if s in dfa.finalstates:
        print("1",end=" ")
    else:
        print("0",end=" ")
print()
for state in dfa.states:
    for letter in alphabets:
        print(letter,end=" ")
        print(changedname[state],end=" ")
        print(changedname[dfa.transitions[state][letter]])
for string in inputstrings:
    r = dfa.accept(string)
    if r[0]:
        print("Yes" ,end=" ")
    else:
        print("No",end=" ")
    for s in r[1]:
        print(changedname[s],end=" ")
    print()




