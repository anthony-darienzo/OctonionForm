import numpy as np
import itertools
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

def fiveForm(a,b,c,d,e):
    return (
    commuAssociator(commutator(a,b),c,d,e) 
    - commutator(commuAssociator(a,b,c,d),e) 
    +  commuAssociator(commutator(e,c),b,d,a)
    - commutator( commuAssociator(e,c,b,d),a)
    )

def fiveFormVanishes(n):
    counter = 0
    combos = list(itertools.permutations(getBasis(n),5))
    length = len(combos)
    print("length:")
    print(length)
    for combo in combos:
        counter += 1
        if (counter%200 == 0):
            print("heartbeat: " + str(counter/length*100) + "percent done")
        if (fiveForm(combo[0],combo[1],combo[2],combo[3],combo[4]).any()):
            print(combo[0], combo[1], combo[2], combo[3],combo[4])
            print(counter)
            return False
    print(counter)
    return True

print("starting")
# print(getBasis(3))
# print(np.array([1])*np.array([2]))
# a = np.array([1,2,0,0])
# b = np.array([3,4,3,2])
# print(CDMult(a,b))

# a = np.array([0,1,0,0])
# b = np.array([0,0,1,0])
# print(CDMult(a,b))


    
# basis = getBasis(3)
#     print(commutator(x,y))
# print(assocVanishes(6))
# print(assocVanishesOld(6))
# print(cAAltVanishes(4))
print(fiveFormVanishes(5))

# for _ in itertools.permutations(getBasis(3)):
#     print(_)
# combos = list(itertools.permutations(getBasis(3),3))
# for combo in combos:
#     print(combo)