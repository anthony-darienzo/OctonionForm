import numpy as np
import itertools
import sys
import time

def conj(x):
    n = len(x)

    if n == 1:
        return x

    m = n // 2
    a, b = x[:m], x[m:]
    z = np.zeros(n)
    z[:m] = conj(a)
    z[m:] = -1*b
    return z

def CDMult(x, y):
    n = len(x)

    if n == 1:
        return x*y

    m = n // 2
    a, b = x[:m], x[m:]
    c, d = y[:m], y[m:]
    z = np.zeros(n)
    z[:m] = CDMult(a, c) - CDMult(conj(d), b)
    z[m:] = CDMult(d, a) + CDMult(b, conj(c))
    return z

# def getBasis(n):
#     if n == 1:
#         return [1]
#     else:
#         # basis = np.empty(2**(n-1), dtype=int)
#         basis = []
#         lowerBasis = getBasis(n-1)
#         for basisElem in lowerBasis:
#             length = 0
#             if (basisElem == 1):
#                 length = 1
#             else:
#                 length = len(basisElem)
#             # basis = np.append(basis,[[basisElem,0],[0,basisElem]])
#             basis.append([basisElem,np.zeros(length,dtype=int).tolist()])
#             basis.append([np.zeros(length,dtype=int).tolist(),basisElem])
#     return basis

def getBasis(n):
    basis = []
    for i in range(2**(n-1)):
        z = np.zeros(2**(n-1),dtype=int)
        z[i] = 1
        basis.append(z)
    return basis

def commutator(x,y):
    return CDMult(x,y) - CDMult(y,x)

def commVanishes(n):
    basis = getBasis(n)
    for x in basis:
        for y in basis:
            if (commutator(x,y).any()):
                print(x,y)
                return False
    return True

def associator(x,y,z):
    return CDMult(x,CDMult(y,z)) - CDMult(CDMult(x,y),z)

def assocVanishesOld(n):
    basis = getBasis(n)
    for x in basis:
        for y in basis:
            for z in basis:
                if (associator(x,y,z).any()):
                    print(x,y,z)
                    return False
    return True

def commuAssociator(a,b,c,d):
    return (
    associator(commutator(a,b),c,d) 
    - commutator(associator(a,b,c),d) 
    + associator(commutator(d,b),c,a)
    - commutator(associator(d,b,c),a))

def cAVanishesOld(n):
    basis = getBasis(n)
    for x in basis:
        for y in basis:
            for z in basis:
                for w in basis:
                    if (commuAssociator(x,y,z,w).any()):
                        print(x,y,z,w)
                        return False
    return True


def assocVanishes(n):
    combos = list(itertools.permutations(getBasis(n),3))
    for combo in combos:
        x, y, z = combo[0], combo[1], combo[2]
        if (associator(x,y,z).any()):
            print(x,y,z)
            return False
    return True

def cAVanishes(n):
    combos = list(itertools.permutations(getBasis(n),4))
    for combo in combos:
        x, y, z, w = combo[0], combo[1], combo[2], combo[3]
        if (commuAssociator(x,y,z,w).any()):
            print(x,y,z,w)
            return False
    return True

def getCANonVanishList(n):
    examplesFound = 0
    counter = 0
    nonVanishList = []
    combos = list(itertools.permutations(getBasis(n),4))
    length = len(combos)
    print("length:")
    print(length)
    for combo in combos:
        counter += 1
        if (counter%200 == 0):
            print("heartbeat: " + str(counter/length*100) + "percent done")
        x, y, z, w = combo[0], combo[1], combo[2], combo[3]
        if (commuAssociator(x,y,z,w).any()):
            examplesFound += 1
            print(examplesFound)
            nonVanishList.append(combo)
    print(examplesFound / counter)
    return nonVanishList


def commuAssociatorAlt(a,b,c,d):
    return (
    associator(commutator(a,b),c,d) 
    - commutator(associator(a,b,c),d) 
    + associator(commutator(d,c),b,a)
    - commutator(associator(d,c,b),a)
    )

def cAAltVanishes(n):
    combos = list(itertools.permutations(getBasis(n),4))
    for combo in combos:
        x, y, z, w = combo[0], combo[1], combo[2], combo[3]
        if (commuAssociatorAlt(x,y,z,w).any()):
            print(x,y,z,w)
            return False
    return True

def fiveFormAlt(a,b,c,d,e):
    return (
    commuAssociator(commutator(a,b),c,d,e) 
    - commutator(commuAssociator(a,b,c,d),e) 
    +  commuAssociator(commutator(e,d),b,a,c)
    - commutator( commuAssociator(e,d,b,a),c)
    )

def fiveFormTest(a,b,c,d,e):
    perm = [4,3,1,2,0]
    elems = [a,b,c,d,e]
    a2 = elems[perm[0]]
    b2 = elems[perm[1]]
    c2 = elems[perm[2]]
    d2 = elems[perm[3]]
    e2 = elems[perm[4]]
    succ = True
    x1 = commutator(a,b)
    if (not x1.any()):
        return np.array([0]), False
    x3 = commutator(a2,b2)
    if (not x3.any()):
        return np.array([0]), False
    x2 = commuAssociator(a,b,c,d)
    if (not x2.any()):
        return np.array([0]), False
    y2 = commutator(x2,e)
    if (not y2.any()):
        return np.array([0]), False
    x4 = commuAssociator(a2,b2,c2,d2)
    if (not x4.any()):
        return np.array([0]), False
    y4 = commutator(x4,e2)
    if (not y4.any()):
        return np.array([0]), False
    y1 = commuAssociator(x1,c,d,e)
    if (not y1.any()):
        return np.array([0]), False
    y3 = commuAssociator(x3,c2,d2,e2)
    if (not y3.any()):
        return np.array([0]), False
    return (y1 - y2 + y3 - y4), True

def fiveForm(a,b,c,d,e, perm):
    if (a[0] == 1):
        return np.array([0]), False
    elems = [a,b,c,d,e]
    a2 = elems[perm[0]]
    b2 = elems[perm[1]]
    c2 = elems[perm[2]]
    d2 = elems[perm[3]]
    e2 = elems[perm[4]]
    succ = True
    x1 = commutator(a,b)
    if (not x1.any()):
        return np.array([0]), False
    x3 = commutator(a2,b2)
    if (not x3.any()):
        return np.array([0]), False
    x2 = commuAssociator(a,b,c,d)
    if (not x2.any()):
        return np.array([0]), False
    y2 = commutator(x2,e)
    if (not y2.any()):
        return np.array([0]), False
    x4 = commuAssociator(a2,b2,c2,d2)
    if (not x4.any()):
        return np.array([0]), False
    y4 = commutator(x4,e2)
    if (not y4.any()):
        return np.array([0]), False
    y1 = commuAssociator(x1,c,d,e)
    if (not y1.any()):
        return np.array([0]), False
    y3 = commuAssociator(x3,c2,d2,e2)
    if (not y3.any()):
        return np.array([0]), False
    return (y1 - y2 + y3 - y4), True

def fiveFormVanishes(n):
    # perms = list(itertools.permutations([0,1,2,3,4]))
    perms = [[4, 3, 1, 0, 2], [4, 3, 1, 2, 0]]
    combos = list(itertools.permutations(getBasis(n),5))
    length = len(combos)
    permCounter = 0
    for perm in perms:
        start = time.time()
        permCounter += 1
        counter = 0
        failure = False
        for combo in combos:
            counter += 1
            if (counter%200 == 0):
                print("heartbeat: " + str(counter/length*100) + " percent done on perm " + str(permCounter))
            test, succ = fiveForm(combo[0],combo[1],combo[2],combo[3],combo[4], perm)
            if (succ != False):
                if (test.any()):
                    failure = True
                    original_stdout = sys.stdout # Save a reference to the original standard output
                    with open('filename.txt', 'a') as f:
                        sys.stdout = f # Change the standard output to the file we created.
                        print("----")
                        print(perm)
                        print(combo[0].tolist(), combo[1].tolist(), combo[2].tolist(), combo[3].tolist(),combo[4].tolist())
                        print("Result:")
                        print(test)
                        print(str(counter/length*100) + " percent done")
                        print("----")
                        sys.stdout = original_stdout # Reset the standard output to its original value
                    break
        if (not failure):
            original_stdout = sys.stdout # Save a reference to the original standard output
            with open('filename.txt', 'a') as f:
                sys.stdout = f # Change the standard output to the file we created.
                print("----")
                print(perm)
                print("VANISHES")
                print("----")
                sys.stdout = original_stdout # Reset the standard output to its original value
        end = time.time()
        print(end - start)

def combinedFiveFormVanishes(n):
    perms = [[0, 1, 4, 2, 3], [3, 2, 4, 0, 1]] 
    counter = 0
    failure = False
    combos = list(itertools.permutations(getBasis(n),5))
    length = len(combos)
    print(length)
    for combo in combos:
        counter += 1
        if (counter%200 == 0):
            print("heartbeat: " + str(counter/length*100) + " percent done")
        test1, succ1 = fiveForm(combo[0],combo[1],combo[2],combo[3],combo[4], perms[0])
        test2, succ2 = fiveForm(combo[0],combo[1],combo[2],combo[3],combo[4], perms[1])
        test = test1 + test2
        if (succ1 != False and succ2 != False):
            if (test.any()):
                failure = True
                original_stdout = sys.stdout # Save a reference to the original standard output
                with open('filename2.txt', 'a') as f:
                    sys.stdout = f # Change the standard output to the file we created.
                    print("----")
                    print(perms[0])
                    print(perms[1])
                    print(combo[0].tolist(), combo[1].tolist(), combo[2].tolist(), combo[3].tolist(),combo[4].tolist())
                    print("Result:")
                    print(test)
                    print(str(counter/length*100) + " percent done")
                    print("----")
                    sys.stdout = original_stdout # Reset the standard output to its original value
                break
    if (not failure):
        original_stdout = sys.stdout # Save a reference to the original standard output
        with open('filename2.txt', 'a') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print("----")
            print("sum of perms VANISHES")
            print("----")
            sys.stdout = original_stdout # Reset the standard output to its original value

print("starting")

# a = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# b = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) 
# c = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# d = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
# e = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
# print(fiveForm(a,b,c,d,e, [1, 0, 4, 2, 3])[0] + fiveForm(a,b,c,d,e, [0, 1, 4, 2, 3])[0])


print(fiveFormVanishes(5))
# print(combinedFiveFormVanishes(5))