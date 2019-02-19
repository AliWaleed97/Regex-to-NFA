import numpy as np
from copy import deepcopy
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

class NFA:
    def __init__(self):
        self.initialState = None
        self.states = set()
        self.finalState = None
        self.transitions = []

    
    def basic(self, input):
        self.initialState = 0
        self.finalState = 1
        self.states.add(self.initialState)
        self.states.add(self.finalState)
        transition = {
            "from" : self.initialState,
            "input" : input,
            "to" : [self.finalState]
        }
        self.transitions.append(transition)
        return self

    def display(self):
        object = {
            "states": self.states,
            "start state": self.initialState,
            "final state": self.finalState,
            "transitions": self.transitions
        }
        print ("states:", self.states)
        print ("start state: ", self.initialState)
        print ("final states:", self.finalState)
        print ("transitions:", self.transitions)
        return object

def basic(input):
    nfa = NFA()
    nfa.initialState = 0
    nfa.finalState = 1
    nfa.states.add(nfa.initialState)
    nfa.states.add(nfa.finalState)
    transition = {
        "from" : nfa.initialState,
        "input" : input,
        "to" : [nfa.finalState]
    }
    nfa.transitions.append(transition)
    return nfa

def concat(nfa1, nfa2):
        nfa = NFA()
        # handle nfa2
        maximum = max(nfa1.states)
        for i in range(0,len(nfa2.transitions)):
            nfa2.transitions[i]['from'] += maximum
            nfa2.transitions[i]['to'] = list(np.add(maximum,nfa2.transitions[i]['to']))
        # handle self
        newStates = np.add(maximum, np.array(list(nfa2.states)))
        newStates = set(set(newStates).union(nfa1.states))
        nfa.states = newStates
        nfa.initialState = nfa1.initialState
        nfa.finalState = nfa2.finalState + maximum
        for transition in nfa1.transitions:
            nfa.transitions.append(transition)
            print("hello", transition)
        for transition in nfa2.transitions:
            nfa.transitions.append(transition)
        return nfa

def union(nfa1, nfa2):
        nfa = NFA()
        # handle nfa1
        newStates1 = np.add(np.array(list(nfa1.states)),1)
        maximum = max(newStates1)
        nfa1.initialState += 1
        nfa1.finalState += 1
        for i in range(0, len(nfa1.transitions)):
            nfa1.transitions[i]['from']+= 1
            nfa1.transitions[i]['to'] = list(np.add(1, nfa1.transitions[i]['to']))
        #handle nfa2
        nfa2.initialState += maximum + 1
        nfa2.finalState += maximum + 1
        newStates2 = np.add(np.array(list(nfa2.states)),maximum + 1)
        for i in range(0, len(nfa2.transitions)):
            nfa2.transitions[i]['from']+= maximum + 1
            nfa2.transitions[i]['to'] = list(np.add(maximum + 1, nfa2.transitions[i]['to']))
        #handle self
        nfa.initialState = 0
        nfa.finalState = nfa2.finalState + 1
        nfa.states.add(nfa.initialState)
        for state in newStates1:
            nfa.states.add(state)
        for state in newStates2:
            nfa.states.add(state)
        nfa.states.add(nfa.finalState)

        initialTransition = {
            "from": nfa.initialState,
            "input": " ",
            "to": [nfa1.initialState, nfa2.initialState]
        }
        finalTransition1 = {
            "from": nfa1.finalState,
            "input": " ",
            "to": [nfa.finalState]
        }
        finalTransition2 = {
            "from": nfa2.finalState,
            "input": " ",
            "to": [nfa.finalState]
        }
        nfa.transitions.append(initialTransition)
        for transition in nfa1.transitions:
            nfa.transitions.append(transition)
        for transition in nfa2.transitions:
            nfa.transitions.append(transition)       
        nfa.transitions.append(finalTransition1)
        nfa.transitions.append(finalTransition2)
        return nfa

def kleene(nfa):
        # #handle nfa
        nfaMain = NFA()
        nfaMain.initialState = 0
        nfa.states = np.add(np.array(list(nfa.states)),1)
        for i in range(0,len(nfa.transitions)):
            nfa.transitions[i]['from'] += 1
            nfa.transitions[i]['to'] = list(np.add(1,nfa.transitions[i]['to']))
        nfa.initialState+=1
        nfa.finalState+=1
        nfaMain.finalState = nfa.finalState + 1
        initialTransition = {
            "from": nfaMain.initialState,
            "input":  " ",
            "to": [nfa.initialState,nfaMain.finalState]
        }
        finalTransition = {
            "from": nfa.finalState,
            "input": " ",
            "to": [nfa.initialState, nfaMain.finalState]
        }
        nfaMain.states.add(nfaMain.initialState)
        nfaMain.states.add(nfaMain.finalState)
        for state in nfa.states:
            nfaMain.states.add(state)
        nfaMain.transitions.append(initialTransition)
        for transition in nfa.transitions:
            nfaMain.transitions.append(transition)
        nfaMain.transitions.append(finalTransition)
        return nfaMain

def plus(nfa):
    nfa1 = deepcopy(nfa)
    nfa2 = deepcopy(nfa)
    star = NFA()
    star = kleene(nfa2)
    result = NFA()
    result = concat(nfa1,star)
    return result

def conditional(nfa):
    # a? = (a|epsilon)
    nfa1 = deepcopy(nfa)
    epsilon = NFA()
    epsilon = epsilon.basic(' ')
    result = NFA()
    result = union(nfa1,epsilon)
    return result

def processRegex(regex):
    # regex = regex.replace('ϵ',' ')
    modified = regex[0]
    for i in range(1,len(regex)):
        if( (((regex[i].isalpha() or regex[i].isdigit() ) and regex[i-1] != '(') or regex[i] == '(') and (regex[i-1] != '|' or regex[i-1] == ')') ):
            modified += '.'+regex[i]
        else:
            modified += regex[i]       
    print (modified )
    return modified

def infix2postfix(regex):
    prec = {}
    prec["*"] = 4
    prec["?"] = 4
    prec["+"] = 4
    prec["."] = 3
    prec["|"] = 2
    prec["("] = 1
    tokens = list(regex)
    output = []
    stack = Stack()
    for token in tokens:
        if (token.isalpha() or token.isdigit() or token == ' '):
            output.append(token)
        elif (token == '('):
            stack.push(token)
        elif (token == ')'):
            top = stack.pop()
            while(top != '('):
                output.append(top)
                top = stack.pop()
        else:
            while (not stack.isEmpty()) and (prec[stack.peek()] >= prec[token]):
                  output.append(stack.pop())
            stack.push(token)
    while(not stack.isEmpty()):
        output.append(stack.pop())
    
    return ''.join(output)

def evaluatePostfix(regex):
    if(len(regex) == 1):
        nfa = NFA()
        nfa = nfa.basic(regex)
        return nfa
    stack = Stack()
    for token in regex:
        if(token.isalpha() or token.isdigit() or token == ' '):
            nfa = NFA()
            nfa = nfa.basic(token)
            stack.push(nfa)
        else:
            if(token == '*'):
                nfa = stack.pop()
                result = kleene(nfa)
                print('*')
                result.display()
                stack.push(result)
            elif(token == '.'):
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                result = concat(nfa1,nfa2)
                print('.')
                result.display()
                stack.push(result)
            elif(token == '|'):
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                result = union(nfa1,nfa2)
                print('|')
                result.display()
                stack.push(result)
            elif(token == '?'):
                nfa = stack.pop()
                result = conditional(nfa)
                print('?')
                result.display()
                stack.push(result)
            elif(token == '+'):
                nfa = stack.pop()
                result = plus(nfa)
                print('+')
                result.display()
                stack.push(result)
    nfa = NFA()
    nfa = stack.pop()
    print (nfa)
    with open('task_2_result.txt', 'w') as f:
        for state in nfa.states:
            f.write(str(state)+", ")
        f.write('\n')
        #for loop language
        lang = []
        for i in range(0,len(nfa.transitions)):
            lang.append(str(nfa.transitions[i]['input']))
        lang = set(lang)
        f.write(str(lang))
        print (lang)
        f.write('\n')
        f.write(str(nfa.initialState))
        f.write('\n')
        f.write(str(nfa.finalState))
        f.write('\n')
        for transition in nfa.transitions:
            f.write(str(transition)+ ", ")

    return nfa

def run(regex):
    processed = processRegex(regex)
    postfix = infix2postfix(processed)
    print(postfix)
    return evaluatePostfix(postfix)

# conditional is the only one to be checked
result = run('(a|b)*ab')
result.display()
