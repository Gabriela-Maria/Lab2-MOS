
#------------------------------------------------------------------------------------------------
#-----------1.1 generar matriz de cobertura------------------------------------------------------

import queen_mapper  
L=['a','b','c','d','e','f','g','h']
N=[8  ,7  ,6  ,4  ,5  ,3  ,2  ,1  ]

def diagonalNegIzqu(ind_i, ind_j,m):
    x=1
    while x< len(N) and (ind_i-x>=0) and (ind_j+x<8):
        m[L[ind_i-x], N[ind_j+x]]=1
        x+=1
        
def diagonalPosIzqu(ind_i, ind_j,m):
    x=1
    while x< len(N) and (ind_i-x>=0) and (ind_j-x>=0):
        m[L[ind_i-x], N[ind_j-x]]=1
        x+=1
        
def diagonalNegDer(ind_i, ind_j,m):
    x=1
    while x< len(N) and (ind_i+x<8) and (ind_j+x<8):
        m[L[ind_i+x], N[ind_j+x]]=1
        x+=1
        
def diagonalPosDer(ind_i, ind_j,m):
    x=1
    while x< len(N) and (ind_i+x<8) and (ind_j-x>=0):
        m[L[ind_i+x], N[ind_j-x]]=1
        x+=1
        
def crearMatriz(pos_i,pos_j):
    matriz={}
    for letra in L:
        index_i = L.index(pos_i)
        for num in N:
            index_j = N.index(pos_j)
            matriz[letra,num]=0
            if (pos_i==letra or pos_j==num):
                matriz[letra,num]=1
    diagonalNegIzqu(index_i, index_j, matriz)
    diagonalPosIzqu(index_i,index_j, matriz)
    diagonalNegDer(index_i, index_j, matriz)
    diagonalPosDer(index_i, index_j, matriz)
    
    return matriz

def imprimirMatriz(matriz):
    print("    " + "  ".join(L)) #letras, eje i
    print("  " + "-" * 25)  

    for num in N:  # numeros, eje j
        fila = [str(matriz[(letra, num)]) for letra in L]
        print(f"{num} | " + "  ".join(fila))  # num de fila y la fila de valores

# matriz = crearMatriz('a', 1) ## ACA poner la posicion del tablero
# imprimirMatriz(matriz)
# print (matriz)
#-------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------
#-----------1.2 generar matriz de cobertura general ---------------------------------------------

def crearMatrizGeneral():
    matriz_general = {}
    for letra in L:
        for num in N:
            matriz_general[(letra, num)] = crearMatriz(letra, num)
    return matriz_general

# Prueba del código
matriz_general = crearMatrizGeneral()

# Imprimir la matriz de una posición específica (por ejemplo, 'a', 1)
# print(matriz_general)

# imprimirMatriz(matriz_general[('h',4)])
#------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------
#-----------3. Implementacion en Pyomo ----------------------------------------------------------

from pyomo.environ import *

# Definimos el modelo
Model = ConcreteModel()

#N = 8

I = Set(initialize=L)  

J = Set(initialize=N) 

Model.x = Var(L,N, domain=Binary)

Model.obj = Objective(expr=sum(Model.x[i, j] for i in L for j in N), sense=minimize)

Model.rest1 = ConstraintList()
for a in L :
    for b in N:
        Model.rest1.add(sum(Model.x[i,j] * matriz_general[(i,j)][(a,b)] for i in L for j in N)>=1)

Model.rest2 = ConstraintList()

Model.rest2.add(sum(Model.x[i,j] * matriz_general[(i,j)][(a,b)] for a in L for b in N for i in L for j in N)>=64)


SolverFactory('glpk').solve(Model)
Model.display()
print ("-------------Solucion-------------")
print("Posiciones de las reinas:")
queen_positions=[]
for i in L:
    for j in N: 
        if Model.x[i, j].value == 1:
            queen_positions.append(f"{i}{j}")
print (queen_positions)
opt_value = value(Model.obj)
print("Valor óptimo (número mínimo de reinas):", opt_value)
#------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------
#-----------5. Visualizacion --------------------------------------------------------------------
queen_mapper.visualize_queens(queen_positions)
#------------------------------------------------------------------------------------------------
