import itertools, numpy
#Importamos la librería itertools ya que utilizaremos un método para realizar combinatorias en el arreglo dado L

def Another_Brute_Force_PDP(L, n):
    max_element = max(L) #Obtenemos el Máximo elemento en el arreglo L
    delta_X = [] 
    X = [] # Declaramos nuestros arreglos para nuestro conjunto Delta X y X

    uniq = numpy.unique(L) # Obtenemos los elementos unicos de L
    combinatorial = list(itertools.combinations(uniq, n-2)) # Realizamos la combinatoria con el arreglo uniq con n-2 elementos
	#El método combinations de intertools tiene dos parametros, el primero es el objeto donde se encuentran los elementos
	# a combinar, el segundo párametro nos indica el número de elementos de cada combinatoria, el método nos regresa un arreglo de las combinaciones finales

    for com in combinatorial: #Se realiza un for para pasar por cada elemento en nuestro arreglo de combinaciones finales 
        X.append(max_element)
        X.append(0)	#Ponemos el primer y máximo elemento obtenido en nuestro conjunto X
        
        for c in com:  # Realizamos un for para obtener cada elemento de combinaciones en el arreglo del objeto en la posición com
            X.append(c)
        X.sort()  # Ordenamos nuestro conjunto X
        
        for i in range(n):  #Realizamos dos for para comparar las distancias que se encuentran desde cada elemento en el conjunto X y se almancena en Delta X
            for j in range(i + 1, n):
                delta_X.append(X[j] - X[i])
            delta_X.sort() # Ordenamos Destal X
        if (L == delta_X): # Comparamos si L = Delta X
            return X
        del X[:] #Eliminamos nuestros conjuntos para limpiar los registros y no generar errores
        del delta_X[:]
    
    return None

L = [2, 2, 3, 3, 4, 5, 6, 7, 8, 10]
n=len(L)/2  
solution = Another_Brute_Force_PDP(L, int(n))
print(solution)

