import sys
from PyQt5 import uic, QtWidgets, QtCore
import random as rn
import math
import copy

qtCreatorFile = "grafico.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btnEmp.clicked.connect(self.calcular)
    
    def veri(self, tablero, numEsp):
        for i in range(3):
            for j in range(3):
                if numEsp == tablero[i][j]:
                    return False
        return True

    def veriL(self, lista, numEsp):
        for i in range(3):
            if numEsp == lista[i]:
                return False
        return True

    def llenarTab(self, tablero):
        for i in range(3):
            for j in range(3):
                numEsp = rn.randint(0, 8)
                while (self.veriL(tablero[i], numEsp) == False) or (self.veri(tablero, numEsp) == False):
                    numEsp = rn.randint(0, 8)
                tablero[i][j] = numEsp


    def findElement(self, elm):
        tabAux = [[1,2,3], [4,5,6], [7,8,0]]
        for i in range(3):
            for j in range(3):
                if elm == tabAux[i][j]:
                    return  [i, j]
        return -1

    def Manhattan(self, tablero):
        acumulate = 0
        for i in range(3):
            for j in range(3):
                pos = self.findElement(tablero[i][j])
                if pos != -1:
                    distance = abs(j-pos[1]) + abs(i-pos[0])
                acumulate += distance
                distance = 0
        return acumulate

    #Funcion para encontrar las coordenadas del espacio vacio
    def findSpace(self, tablero):
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == 0:
                    return (i, j)
        return None

    #Funcion para escoger un vecino random del espacio en blanco
    def randomNeighbor(self, posSpace):
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
    def generateNewState(self, tablero):
        tab = copy.deepcopy(tablero)
        space = self.findSpace(tab)
        neigh = self.randomNeighbor(space)
        aux = tab[space[0]][space[1]]
        tab[space[0]][space[1]] = tab[neigh[0]][neigh[1]]
        tab[neigh[0]][neigh[1]] = aux
        return tab

    def llenarCurrent(self, tablero):
        self.txt1_1.setText(str(tablero[0][0]))
        self.txt2_1.setText(str(tablero[0][1]))
        self.txt3_1.setText(str(tablero[0][2]))
        self.txt4_1.setText(str(tablero[1][0]))
        self.txt5_1.setText(str(tablero[1][1]))
        self.txt6_1.setText(str(tablero[1][2]))
        self.txt7_1.setText(str(tablero[2][0]))
        self.txt8_1.setText(str(tablero[2][1]))
        self.txt9_1.setText(str(tablero[2][2]))
    
    def llenarBest(self, tablero):
        self.txt1_2.setText(str(tablero[0][0]))
        self.txt2_2.setText(str(tablero[0][1]))
        self.txt3_2.setText(str(tablero[0][2]))
        self.txt4_2.setText(str(tablero[1][0]))
        self.txt5_2.setText(str(tablero[1][1]))
        self.txt6_2.setText(str(tablero[1][2]))
        self.txt7_2.setText(str(tablero[2][0]))
        self.txt8_2.setText(str(tablero[2][1]))
        self.txt9_2.setText(str(tablero[2][2]))

    def llenarNew(self, tablero):
        self.txt1_3.setText(str(tablero[0][0]))
        self.txt2_3.setText(str(tablero[0][1]))
        self.txt3_3.setText(str(tablero[0][2]))
        self.txt4_3.setText(str(tablero[1][0]))
        self.txt5_3.setText(str(tablero[1][1]))
        self.txt6_3.setText(str(tablero[1][2]))
        self.txt7_3.setText(str(tablero[2][0]))
        self.txt8_3.setText(str(tablero[2][1]))
        self.txt9_3.setText(str(tablero[2][2]))

    def calcular(self):
        tablero = [[None]*3 for i in range(3)]
        self.llenarTab(tablero)

        Temp = 10000
        Speed = 0.005
        Current = copy.deepcopy(tablero)
        Best = copy.deepcopy(tablero)
        New = copy.deepcopy(tablero)

        CurrentEnergy = self.Manhattan(Current)
        BestEnergy = CurrentEnergy

        self.llenarCurrent(Current)
        self.llenarBest(Best)
        self.llenarNew(New)

        while Temp > 1:
            New = self.generateNewState(Current)
            CurrentEnergy = self.Manhattan(Current)
            NewEnergy = self.Manhattan(New)

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

            self.llenarCurrent(Current)
            print(Current)
            self.llenarBest(Best)
            print(Best)
            self.llenarNew(New)
            print(New)
            print('-----------------------')

            self.energy.setText(str(BestEnergy))
            self.temperatura.setText(str(int(Temp)))

        
if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())