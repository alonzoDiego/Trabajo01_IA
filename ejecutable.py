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
        self.dates()
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
        
    def dates(self):
        self.tablero = [[None]*3 for i in range(3)]
        self.llenarTab(self.tablero)
        
        self.Temp = 10000
        self.Speed = 0.005
        self.Current = copy.deepcopy(self.tablero)
        self.Best = copy.deepcopy(self.tablero)
        self.New = copy.deepcopy(self.tablero)

        self.CurrentEnergy = self.Manhattan(self.Current)
        self.BestEnergy = self.CurrentEnergy

        self.llenarCurrent(self.Current)
        self.llenarBest(self.Best)
        self.llenarNew(self.New)
        self.energy.setText(str(self.BestEnergy))
        self.temperatura.setText(str(int(self.Temp)))
    
    def calcular(self):
        
        self.dates()

        while self.Temp > 1:
            self.New = self.generateNewState(self.Current)
            self.CurrentEnergy = self.Manhattan(self.Current)
            self.NewEnergy = self.Manhattan(self.New)

            #Funcion Aceptacion
            if self.NewEnergy < self.CurrentEnergy:
                Prob = 1
            else:
                expo = -((self.CurrentEnergy-self.NewEnergy) / self.Temp)
                if expo <= 230:
                    Prob = math.exp(expo)
                else: Prob = 0.35
            if Prob > rn.random():
                self.Current = copy.deepcopy(self.New)
                self.CurrentEnergy = self.NewEnergy

            #Actualizacion temp y mejor solucion
            if self.CurrentEnergy < self.BestEnergy:
                self.BestEnergy = self.CurrentEnergy
                self.Best = copy.deepcopy(self.Current)

            self.Temp = (1 - self.Speed) * self.Temp

            self.llenarCurrent(self.Current)
            print(self.Current)
            self.llenarBest(self.Best)
            print(self.Best)
            self.llenarNew(self.New)
            print(self.New)
            print("Energy: ", self.BestEnergy)
            print("Temp: ", int(self.Temp))
            print('-----------------------')

            self.energy.setText(str(self.BestEnergy))
            self.temperatura.setText(str(int(self.Temp)))

        
if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())