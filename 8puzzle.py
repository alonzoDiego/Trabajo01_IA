import random as rn
import math
import copy

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

#Funcion para encontrar las coordenadas del espacio vacio
def findSpace(tablero):
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == 0:
                return (i, j)
    return None

#Funcion para escoger un vecino random del espacio en blanco
def randomNeighbor(posSpace):
    cond1 = rn.choice([-1,1])
    cond2 = rn.choice([True, False])
    while(True):
        if cond2:
            if posSpace[0] + cond1 >= 0 and posSpace[0] + cond1 <= 2:
                return (posSpace[0] + cond1, posSpace[1])
        else:
            if posSpace[1] + cond1 >= 0 and posSpace[1] + cond1 <= 2:
                return (posSpace[0], posSpace[1] + cond1)
        cond1 = rn.choice([-1,1])
        cond2 = rn.choice([True, False])
    
#Funcion que genera un nuevo tablero moviendo una pieza al espacio en blanco
def generateNewState(tablero):
    tab = copy.deepcopy(tablero)
    space = findSpace(tab)
    neigh = randomNeighbor(space)
    aux = tab[space[0]][space[1]]
    tab[space[0]][space[1]] = tab[neigh[0]][neigh[1]]
    tab[neigh[0]][neigh[1]] = aux
    return tab


#---------------ALGORITMO---------------------------

tablero = [[None]*3 for i in range(3)]
llenarTab(tablero)

Temp = 10000
Speed = 0.0003
Current = copy.deepcopy(tablero)
Best = copy.deepcopy(tablero)
New = copy.deepcopy(tablero)

CurrentEnergy = Manhattan(Current)
BestEnergy = CurrentEnergy

print(Current)
print(Best)
print(New)

while Temp > 1:
    New = generateNewState(Current)
    CurrentEnergy = Manhattan(Current)
    NewEnergy = Manhattan(New)

    #Funcion Aceptacion
    if NewEnergy < CurrentEnergy:
        Prob = 1
    else:
        expo = -((CurrentEnergy-NewEnergy) / Temp)
        if expo <= 230:
            Prob = math.exp(expo)
        else: Prob = 0.35
    if Prob > rn.random():
        Current = copy.deepcopy(New)
        CurrentEnergy = NewEnergy

    #Actualizacion temp y mejor solucion
    if CurrentEnergy < BestEnergy:
        BestEnergy = CurrentEnergy
        Best = copy.deepcopy(Current)

    Temp = (1 - Speed) * Temp

    print('--------------LUEGO-------------')

    print(Current)
    print(Best)
    print(New)
    print('Energia minima: %i' %BestEnergy)
    print('Temperatura: %i' %Temp)

print('------------END------------')