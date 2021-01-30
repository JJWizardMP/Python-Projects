import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Funciones Para graficar segmentos
def dibuja_rectas(col="b"):
    n = len(segs) #segs es global
    #grafica los segmentos de recta generados
    for i in range(n):
        plt.plot([segs.iloc[i]["x_inf"],segs.iloc[i]["x_sup"]],[segs.iloc[i]["y_inf"],segs.iloc[i]["y_sup"]],c = col) 
    for i in range(n):
        plt.scatter([segs.iloc[i]["x_inf"],segs.iloc[i]["x_sup"]],[segs.iloc[i]["y_inf"],segs.iloc[i]["y_sup"]],c = col) 
        
def dibuja_recta(i=0, col="r"):    
    plt.plot([segs.iloc[i]["x_inf"],segs.iloc[i]["x_sup"]],[segs.iloc[i]["y_inf"],segs.iloc[i]["y_sup"]],c = col) 
    plt.scatter([segs.iloc[i]["x_inf"],segs.iloc[i]["x_sup"]],[segs.iloc[i]["y_inf"],segs.iloc[i]["y_sup"]],c = col) 
    
def dibuja_rectangulo(p1, p2, col="r"):
    x_1 = p1[0]
    x_2 = p2[0]
    y_1 = p1[1]
    y_2 = p2[1]
    plt.plot([x_1,x_2],[y_1,y_1],col)         
    plt.plot([x_2,x_2],[y_1,y_2],col)         
    plt.plot([x_2,x_1],[y_2,y_2],col)         
    plt.plot([x_1,x_1],[y_2,y_1],col)    

def dibuja_intersecciones(inter):
	#plt.title("Barrido de Linea Ordenado por la" + med)
	plt.scatter(np.array(inter.x), np.array(inter.y), c="k",  marker='x')
    
# Funciones necesarias para los barridos
def Intersect(i,j,segs):
	x=( (segs.iloc[j]['b']-segs.iloc[i]['b']) / (segs.iloc[i]['m']-segs.iloc[j]['m']) )
	y=( segs.iloc[i]['m']*x+segs.iloc[i]["b"] )
	k1 = np.logical_and( np.logical_and(x>segs.iloc[i]["domin"], segs.iloc[i]["domax"]>x), np.logical_and(x>segs.iloc[j]["domin"], segs.iloc[j]["domax"]>x) )
	k2 = np.logical_and( np.logical_and(y>segs.iloc[i]["y_inf"], segs.iloc[i]["y_sup"]>y), np.logical_and(y>segs.iloc[j]["y_inf"], segs.iloc[j]["y_sup"]>y) )
	if (np.logical_and(k1,k2)):
		return (True ,np.array([x, y]))
	else:
		return (False, None)
        
def ver_int(arrint, ind):
	q = '((seg1 ==' + str(ind[0]) + ')&(seg2 ==' + str(ind[1]) + '))|'
	q = q + '((seg1 ==' + str(ind[1]) + ')&(seg2 ==' + str(ind[0]) + '))'
	qr = arrint.query(q)
	if not qr.empty:
		return True
	return False

def Checkstate(ls, est, segs, evinter, inter, arrint, c, so ):
	n = 0
	for c1, c2 in zip( ls, est):
		if c1 != c2:
			if so == 1:
				c, evinter, inter, arrint = ver_vecinos(n, segs, est, evinter, inter, arrint, c)
			else:
				c, evinter, inter, arrint = ver_vecinosy(n, segs, est, evinter, inter, arrint, c)                
		n +=1
	return (c, evinter, inter, arrint)    
    
# Barrido de Linea Ordenado por la abscisa

def ver_estado(ev, est, segs, evinter, inter, arrint, c):
	sts = pd.DataFrame(columns=['i', 'x']) # DF de soporte para ordenar siempre por abscisa
	for st in est:
		dic = { 'i':st , 'x': (ev['y'] - segs.loc[int(round(st))]['b'])/(segs.loc[int(round(st))]['m'])}
		sts = sts.append(dic, ignore_index=True, sort=False)
	sts = sts.sort_values(by=["x"], ascending=True)
	sts.reset_index(drop=True, inplace=True)
	esprv = list(est[:])
	est=list(sts.i)
	c, evinter, inter, arrint = Checkstate(esprv, est, segs, evinter, inter, arrint, c, 1 )
	ver = True
	l = 0
	while (ver):
		if (l < len(est)):
			if ( sts.iloc[l]['x'] <= ev['x'] ):
				l+=1
			else:
				i=l
				ver = False
		else:
			i=l
			ver = False
	est.insert(i, ev['i'])
	return (list(est), evinter, inter, arrint, c)

def ope_inter(i, j, segs, est, evinter, inter, arrint, c):
    ver = ver_int(arrint, np.array( [int(round(est[i])), int(round(est[j]))]))
    if not ver:
        dic= {'seg1': int(round(est[i])), 'seg2': int(round(est[j]))}
        arrint = arrint.append(dic, ignore_index=True, sort=False)
        arrint = arrint.drop_duplicates()
    if not ver:
        k, p = Intersect(int(round(est[i])),int(round(est[j])), segs) 
        c += 1
        if k :    
            dic= {'x':p[0], 'y':p[1], 'seg1': int(round(est[i])), 'seg2': int(round(est[j]))}
            evinter = evinter.append(dic, ignore_index=True, sort=False)
            evinter = evinter.sort_values(by=["y"], ascending=False)
            evinter.reset_index(drop=True, inplace=True)
            inter = inter.append(dic, ignore_index=True, sort=False)
    return (c, evinter, inter, arrint)

def ver_vecinos(i, segs, est, evinter, inter, arrint, c):
    if ( np.logical_and( i>0, i<len(est)-1) ): # Caso 3
        c, evinter, inter, arrint = ope_inter(i, i-1, segs, est, evinter, inter, arrint, c)
        c, evinter, inter, arrint = ope_inter(i, i+1, segs, est, evinter, inter, arrint, c)
    elif ( i==0 ): # Caso 1
        c, evinter, inter, arrint = ope_inter(i, i+1, segs, est, evinter, inter, arrint, c)
    elif ( i==len(est)-1): # Caso 2
        c, evinter, inter, arrint = ope_inter(i, i-1, segs, est, evinter, inter, arrint, c)
    return (c, evinter, inter, arrint)
    
def eval_evento(ev, est, segs, evinter, inter, arrint, c):
    if not ev['i'] in est: # Evento Punto Superior
        est, evinter, inter, arrint, c=ver_estado(ev, est, segs, evinter, inter, arrint, c)
        indx = est.index(int(round(ev['i'])))
        c, evinter, inter, arrint = ver_vecinos(indx, segs, est, evinter, inter, arrint, c)
    else:  # Evento Punto Inferior
        indx = est.index(int(round(ev['i'])))
        est.remove(ev['i'])
        if ( np.logical_and(indx>0, indx<len(est)-1) ):
            c, evinter, inter, arrint = ope_inter(indx, indx-1, segs, est, evinter, inter, arrint, c)
    return (c, list(est) , evinter, inter, arrint)

def eval_evint(est, segs, evinter, inter, arrint, c):
    # Evento de Interseccion
    va1=evinter.iloc[0]['seg1']
    va2=evinter.iloc[0]['seg2']
    ind1 = est.index(va1)
    ind2 = est.index(va2)
    mn = ind1 if (ind2 > ind1) else ind2
    mx = ind2 if (ind2 > ind1) else ind1
    #Swap
    swp = est[ind2]
    est[ind2] = est[ind1]
    est[ind1] = swp
    evinter.drop([0], inplace=True)
    evinter.reset_index(drop=True, inplace=True)
    c, evinter, inter, arrint = ver_vecinos(mn, segs, est, evinter, inter, arrint, c)
    c, evinter, inter, arrint = ver_vecinos(mx, segs, est, evinter, inter, arrint, c)
    return (c, est, evinter, inter, arrint)

def Barrido_de_Linea_Abscisa(segs, eventos):
    est = [] #estado
    evinter = pd.DataFrame(columns=['x', 'y', 'seg1', 'seg2']) # Eventos de Intersecciones
    inter = evinter# Df que guarda la abscisa y la ordenada de las intersecciones encontradas con el id de los segmentos evaluados
    arrint = pd.DataFrame(columns=['seg1', 'seg2']) # DF que guarda la pareja de Intersecciones ya evaluadas
    n_evs = 0 
    for i, ev in eventos.iterrows():
    	#print est
        if evinter.empty:
            if not est: #Primer Caso el estado esta vacio y el df de intersecciones de igual forma
                est.append(ev['i'])
            else: # El estado posee al menos un elemento
                n_evs, est, evinter, inter, arrint = eval_evento(ev, est, segs, evinter, inter, arrint, n_evs)
        else: # Lista de eventos actualizado con intersecciones
            k=True
            while(k):
                if not evinter.empty:
                    if ( ev['y'] > evinter.iloc[0]['y'] ):
                        n_evs, est, evinter, inter, arrint = eval_evento(ev, est, segs, evinter, inter, arrint, n_evs)
                        k=False
                    else: # Estado cuando se encuentra una interseccion en los eventos
                        n_evs, est, evinter, inter, arrint = eval_evint(est, segs, evinter, inter, arrint, n_evs)
                else: 
                    n_evs, est, evinter, inter, arrint = eval_evento(ev, est, segs, evinter, inter, arrint, n_evs)
                    k=False
    return (inter)
    
# Barrido de Linea Ordenado por la Ordenada
def ver_estadoy(ev, est, segs, evinter, inter, arrint, c):
	sts = pd.DataFrame(columns=['i', 'y']) # DF de soporte para ordenar siempre por ordenada
	for st in est:
		dic = { 'i':st , 'y': (ev['x']*(segs.loc[int(round(st))]['m']) + segs.loc[int(round(st))]['b']) }
		sts = sts.append(dic, ignore_index=True, sort=False)
	sts = sts.sort_values(by=["y"], ascending=True)
	sts.reset_index(drop=True, inplace=True)
	esprv = list(est[:])
	est=list(sts.i)
	c, evinter, inter, arrint = Checkstate(esprv, est, segs, evinter, inter, arrint, c, 0 )
	ver = True
	l = 0
	while (ver):
		if (l < len(est)):
			if ( sts.iloc[l]['y'] <= ev['y'] ):
				l+=1
			else:
				i=l
				ver = False
		else:
			i=l
			ver = False
	est.insert(i, ev['i'])
	return (list(est), evinter, inter, arrint, c)
	
def ope_intery(i, j, segs, est, evinter, inter, arrint, c):
	ver = ver_int(arrint, np.array( [int(round(est[i])), int(round(est[j]))]))
	if not ver:
		dic= {'seg1': int(round(est[i])), 'seg2': int(round(est[j]))}
		arrint = arrint.append(dic, ignore_index=True, sort=False)
		arrint = arrint.drop_duplicates()
	if not ver:
		k, p = Intersect(int(round(est[i])),int(round(est[j])), segs) 
		c += 1
		if k :    
			dic= {'x':p[0], 'y':p[1], 'seg1': int(round(est[i])), 'seg2': int(round(est[j]))}
			evinter = evinter.append(dic, ignore_index=True, sort=False)
			evinter = evinter.sort_values(by=["x"], ascending=True)
			evinter.reset_index(drop=True, inplace=True)
			inter = inter.append(dic, ignore_index=True, sort=False)
	return (c, evinter, inter, arrint)

def ver_vecinosy(i, segs, est, evinter, inter, arrint, c):
	if ( np.logical_and( i>0, i<len(est)-1) ): # Caso 3
		c, evinter, inter, arrint = ope_intery(i, i-1, segs, est, evinter, inter, arrint, c)
		c, evinter, inter, arrint = ope_intery(i, i+1, segs, est, evinter, inter, arrint, c)
	elif ( i==0 ): # Caso 1
		c, evinter, inter, arrint = ope_intery(i, i+1, segs, est, evinter, inter, arrint, c)
	elif ( i==len(est)-1): # Caso 2
		c, evinter, inter, arrint = ope_intery(i, i-1, segs, est, evinter, inter, arrint, c)
	return (c, evinter, inter, arrint)

def eval_eventoy(ev, est, segs, evinter, inter, arrint, c):
	if not ev['i'] in est: # Evento Punto Izquierdo
		est, evinter, inter, arrint, c=ver_estadoy(ev, est, segs, evinter, inter, arrint, c)
		indx = est.index(int(round(ev['i'])))
		c, evinter, inter, arrint = ver_vecinosy(indx, segs, est, evinter, inter, arrint, c)
	else:  # Evento Punto Derecho
		indx = est.index(int(round(ev['i'])))
		est.remove(ev['i'])
		if ( np.logical_and(indx>0, indx<len(est)-1) ):
			c, evinter, inter, arrint = ope_intery(indx, indx-1, segs, est, evinter, inter, arrint, c)
	return (c, list(est) , evinter, inter, arrint)

def eval_evinty(est, segs, evinter, inter, arrint, c):
    # Evento de Interseccion
	va1=evinter.iloc[0]['seg1']
	va2=evinter.iloc[0]['seg2']
	ind1 = est.index(va1)
	ind2 = est.index(va2)
	mn = ind1 if (ind2 > ind1) else ind2
	mx = ind2 if (ind2 > ind1) else ind1
    #Swap
	swp = est[ind2]
	est[ind2] = est[ind1]
	est[ind1] = swp
	evinter.drop([0], inplace=True)
	evinter.reset_index(drop=True, inplace=True)
	c, evinter, inter, arrint = ver_vecinosy(mn, segs, est, evinter, inter, arrint, c)
	c, evinter, inter, arrint = ver_vecinosy(mx, segs, est, evinter, inter, arrint, c)
	return (c, est, evinter, inter, arrint)

def Barrido_de_Linea_Ordenada(segs, eventos):
	est = [] #estado
	evinter = pd.DataFrame(columns=['x', 'y', 'seg1', 'seg2']) # Eventos de Intersecciones
	inter = evinter# Df que guarda la abscisa y la ordenada de las intersecciones encontradas con el id de los segmentos evaluados
	arrint = pd.DataFrame(columns=['seg1', 'seg2']) # DF que guarda la pareja de Intersecciones ya evaluadas
	n_evs = 0 
	for i, ev in eventos.iterrows():
		#print est
		if evinter.empty:
			if not est: #Primer Caso el estado esta vacio y el df de intersecciones de igual forma
				est.append(ev['i'])
			else: # El estado posee al menos un elemento
				n_evs, est, evinter, inter, arrint = eval_eventoy(ev, est, segs, evinter, inter, arrint, n_evs)
		else: # Lista de eventos actualizado con intersecciones
			k=True
			while(k):
				if not evinter.empty:
					if ( ev['x'] < evinter.iloc[0]['x'] ):
						n_evs, est, evinter, inter, arrint = eval_eventoy(ev, est, segs, evinter, inter, arrint, n_evs)
						k=False
					else: # Estado cuando se encuentra una interseccion en los eventos
						n_evs, est, evinter, inter, arrint = eval_evinty(est, segs, evinter, inter, arrint, n_evs)
				else: 
					n_evs, est, evinter, inter, arrint = eval_eventoy(ev, est, segs, evinter, inter, arrint, n_evs)
					k=False
	return (inter)
