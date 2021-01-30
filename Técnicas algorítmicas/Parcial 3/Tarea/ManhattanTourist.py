import sys
import numpy as np

def ManhattanTourist(wc, wr, n, m):
	s=np.zeros((n+1,m),dtype=int) 	#Creación de una matriz que representa los nodos de las distancias
	for i in range(1,n+1):	#Se añade las distancias máximas en la primera fila
		s[i][0]= s[i-1][0] + wr[i-1][0]
	for j in range(1,m):	#Se añade las distancias máximas en la primera columna
		s[0][j]= s[0][j-1] + wc[0][j-1]
	for i in range(1, n+1):	#Fors anidados que se encarga de colocar las distancias de cada fila y columna restante
		for j in range(1,m):
			s[i][j] = Max(s[i-1][j] + wr[i-1][j] , s[i][j-1] + wc[i][j-1] )
	print(s)	# Imprimimos la matriz de las distancias máximas
	return s[n][m-1]	#Regresamos la mayor distancia obtenida
def Max(a,b): #Función que regresa el mayor de dos números
	if(a>b):
		return a
	else:
		return b 
def main():
	wr = [ [1,0,2,4,3], [4,6,5,2,1], [4,4,5,2,1], [5,6,8,5,3] ]	#Matriz que representa las filas
	wc = [ [3,2,4,0], [3,2,4,2], [0,7,3,4], [3,3,0,2], [1,3,2,2] ]	#Matriz que representa las columnas
	s=ManhattanTourist(wc, wr, len(wr), len(wc))	# n es el tamaño de las filas y m el tamaño de las columnas
	print(s)	
	return 0

if __name__ == "__main__":
	sys.exit(int(main() or 0))