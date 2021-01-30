import sys
import numpy as np

def ManhattanTouristDP(wc, wr, n, m):
	s=np.zeros((n+1,m)) 	
	for i in range(1,n+1):	
		s[i][0]= s[i-1][0] + wr[i-1][0]
	for j in range(1,m):	
		s[0][j]= s[0][j-1] + wc[0][j-1]
	for i in range(1, n+1):
		for j in range(1,m):
			s[i][j] = Max(s[i-1][j] + wr[i-1][j] , s[i][j-1] + wc[i][j-1] )
	print(s)	
	return s[n][m-1]

def ManhattanTouristVoraz(dis, x, y):
	wc=dis[0]
	wr=dis[1]
	n=len(wr)
	m=len(wc)
	s=np.zeros((n+1,m)) 	
	ver=False
	i=0
	j=0
	r=0
	while (ver!=True):
		if (i==x):
			r=r+wr[i][j+1]
			ver=True
		elif(j==y):
			r=r+wr[i+1][j]
			ver=True
		else:
			r, var=Max2(r,s[i][j] + wr[i][j],s[j][i] + wc[j][i])
			if var==True:
				j=j+1
			else:
				i=i+1
	print(s)		
	return r

def Max(a,b):
	if(a>b):
		return a
	else:
		return b 
def Max2(r,a,b):
	if(a>b):
		return r+a, True
	else:
		return r+b, False
def main():
	wr = [  [3.02,2.04,2.09,2.04,3.03,2.05,2.05], #Matriz que representa las filas
		[2.04,2.05,2.01,2.1,3.1,2.04,2.06], 
		[3.05,2.09,2.07,2.08,3.03,2.02,3.05], 
		[3.05,3.09,3.08,3.05,3.03,3.1,2.06], 
		[2.03,3.05,3.06,2.09,2.07,3.02,3.04], 
		[2.08, 2.07, 3.1, 2.02,3.05,2.1,2.07] ]	
	wc = [  [3.1,2.07,2.01,3.1,2.06,3.04], #Matriz que representa las columnas
		[3.04,2.02,3.1,2.09,2.08,2.03], 
		[2.02,3.05,3.01,2.09,2.09,2.04], 
		[2.07,3.05,2.01,2.01,3.04,3.05], 
		[2.05,2.1,2.09,2.05,3.08,3.07], 
		[2.05,2.08,3.03,2.09,3.09,3.1], 
		[2.08,3.06,2.01,2.1,2.02,2.06] ]	
	dis=[]
	dis.append(wc)
	dis.append(wr)

	print("Estrategia Voraz:")
	s=ManhattanTouristVoraz(dis,1,1)
	print(s)
	print("Programación Dinámica:")
	s=ManhattanTouristDP(wc, wr, len(wr), len(wc))	
	print(s)	
	return 0

if __name__ == "__main__":
	sys.exit(int(main() or 0))
