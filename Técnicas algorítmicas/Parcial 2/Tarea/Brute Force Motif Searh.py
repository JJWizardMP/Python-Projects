import sys
import numpy as np

def GetDNAMatriz(namefile):
	DNA_Matriz = []
	l = 0
	for line in open(namefile).readlines():
		DNA_Matriz.append(list(line)[0:len(line)-1])
		l +=1
	n=len(DNA_Matriz[0])
	return DNA_Matriz,l,n

def BRUTE_FORCE_MOTIF_SEARCH(DNA_Sample, l):
	lim = len(DNA_Sample[0]) - l + 1
	bestScore = 0
	s = [] ; bestMotif = []
	for a in range(lim):
		for b in range(lim):
			for c in range(lim):
				for d in range(lim):
					for e in range(lim):
						for f in range(lim):
							for g in range(lim):
								s = [a,b,c,d,e,f,g]
								if (Score(s,DNA_Sample,l) > bestScore):
									bestScore = Score(s,DNA_Sample,l)
									bestMotif = s.copy()
	return bestScore, bestMotif

def alignment(matriz, l, Si):
	align = []
	for i, line in enumerate(matriz):
		align.append(line[Si[i]:Si[i]+l])
	return align

def profile(matriz):
	DNA = [['A', 'a'], ['T', 't'], ['G','g'], ['C', 'c']]
	ls=np.asarray(matriz).transpose().tolist()
	#print("Transpose:",ls, sep =" ")
	prof = []
	for i in ls:
		temp = []
		for j in DNA:
			temp.append(i.count(j[0])+i.count(j[1]))
		prof.append(temp)
	return prof

def consensus(matriz):
	DNA = ['A', 'T', 'G', 'C']
	ls = []
	ne = []
	for i in matriz:
		ma = np.argmax(np.array(i))
		m = max(i)
		ls.append(DNA[ma])
		ne.append(m)
	return ls, ne

def score(lista):
	s = 0
	for i in lista:
		s+=i
	return s	

def BRUTE_FORCE_MOTIF_SEARCH_AGAIN(DNA, t, n, l):
	s=np.zeros(t, dtype=int)
	bestMotif= []
	bestscore=Score(s,DNA,l)
	while True:
		s = NEXTLEAF(s, t, n - l )
		"""print("S:",s, sep=" ")
		print("Best Motif:",bestMotif,sep=" ")
		print("Best Score:",bestscore, sep=" ")"""
		if (Score(s, DNA,l) > bestscore):
			bestscore = Score(s, DNA,l)
			bestMotif = s.copy()
		if (np.array_equal(s, np.zeros(t, dtype=int))):
			return bestMotif,bestscore

def Score(s, DNA, l):
	align = []; prof = []; consen = []; consensusn = []
	align = alignment(DNA, l, s)
	prof=profile(align)
	consen, consensusn=consensus(prof)
	return score(consensusn)

def NEXTLEAF(a,L,k):
	for i in reversed(range(L)):
		if (a[i] < k):
			a[i] = a[i] + 1
			return a
		a[i]=0
	return a
	
def ALLLEAVES(L, k):
	a = list((np.zeros(L, dtype=int)))
	while True:
		print(a)
		a = NEXTLEAF(a,L,k-1)
		if (list((np.zeros(L, dtype=int))) == a):
			return None
def NEXTVERTEX(a,i,L,k):
	if (i<L):
		a[i+1]=1
		return a, i+1
	else:
		for j in reversed(range(L)):
			if (a[j] < k):
				a[j]=a[j]+1
				return a,j
	return a,0

def BYPASS(a,i,L,k):
	for j in reversed(range(i)):
		if(a[j]<l):
			a[j]=a[j]+1
			return a,j
	return a,0

def main():
	t=0;n=0;l=2;sco=0
	solution=[]
	conse = []
	sample, t, n = GetDNAMatriz("DNA")
	sco, conse = BRUTE_FORCE_MOTIF_SEARCH(sample, l)
	print("BRUTE FORCE MOTIF SEARCH")
	print("Best Score:", sco, sep=" ")
	print("Best Motif:", conse, sep=" ")
	solution,sco=BRUTE_FORCE_MOTIF_SEARCH_AGAIN(sample,t,n,l)
	print("BRUTE FORCE MOTIF SEARCH AGAIN")
	print("Best Score",sco,sep=" ")
	print("Best Motif:",solution,sep=" ")

if __name__ == "__main__":
	sys.exit(int(main() or 0))