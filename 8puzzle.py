import random as rn
import math

tablero = [[None]*3 for i in range(3)]

def veri(tablero, numEsp):
    for i in range(3):
        for j in range(3):
            if numEsp == tablero[i][j]:
                return False
    return True

def veriL(lista, numEsp):
    for i in range(3):
        if numEsp == lista[i]:
            return False
    return True

def llenarTab(tablero):
    for i in range(3):
        for j in range(3):
            numEsp = rn.randint(0, 8)
            while (veriL(tablero[i], numEsp) == False) or (veri(tablero, numEsp) == False):
                numEsp = rn.randint(0, 8)

            tablero[i][j] = numEsp
    
    print(tablero)

llenarTab(tablero)
######################################

def findElement(elm):
    tabAux = [[1,2,3], [4,5,6], [7,8,0]]
    for i in range(3):
        for j in range(3):
            if elm == tabAux[i][j]:
                return  [i, j]
    return -1

def Manhattan(tablero):
    acumulate = 0

    for i in range(3):
        for j in range(3):
            pos = findElement(tablero[i][j])
            if pos != -1:
                distance = abs(j-pos[1]) + abs(i-pos[0])
            acumulate += distance
            distance = 0

    return acumulate

print(Manhattan(tablero))


