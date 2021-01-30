import sys
import numpy as np
import math

def GetDNAMatriz(namefile):
	DNA_Matriz = []
	t = 0
	for line in open(namefile).readlines():
		DNA_Matriz.append(list(line)[0:len(line)-1])
		t +=1
	n=len(DNA_Matriz[0])
	return DNA_Matriz,t,n

def HammingDistance(str1, str2): 
	diffs = 0
	for ch1, ch2 in zip(str1, str2):
		if (ch1 != ch2):
			diffs += 1
	return diffs

def TotalDistance(v, DNA):
	dist = 0
	for line in DNA:
		minhamming = len(v)
		for i in range(len(line)-len(v)+1):
			h = HammingDistance(v, line[i:i+len(v)])
			if (h < minhamming):
				minhamming = h
		dist += minhamming
	return dist

def NextVertex(a,i,L,k):
	if (i<L):
		a[i]=0
		return a, i+1
	else:
		for j in reversed(range(L)):
			if (a[j] < k-1):
				a[j]=a[j]+1
				return a,j+1
	return a,0

def ByPass(a,i,L,k):
	for j in reversed(range(i)):
		if(a[j]<k-1):
			a[j]=a[j]+1
			return a,j+1
	return a,0

def GetNucleotide(s, i):
	num2dna={0:'A', 1:'C', 2:'G', 3:'T'}
	pre = []
	for xi in s[0:i]:
		pre.append(num2dna[xi])
	return pre
	
def BranchAndBoundMedianSearch(DNA, t, n, l):
	s = list(np.zeros(l, dtype=int))
	bd = math.inf; opd= 0;
	prefix= []; word= []; bw= [];
	i=1 #lvl
	while (i>0):
		if (i<l):
			prefix=GetNucleotide(s, i)
			opd = TotalDistance(prefix, DNA)
			if (opd > bd):
				s, i = ByPass(s,i,l,4)
			else:
				s, i = NextVertex(s,i,l,4)
		else:
			word=GetNucleotide(s, l)
			if ( TotalDistance(word,DNA) < bd ):
				bd = TotalDistance(word, DNA)
				bw = word.copy()
			s, i = NextVertex(s,i,l,4)
	return (bw)

def main():
	t=0;n=0;l=4
	bestword= [] 
	DNA, t, n = GetDNAMatriz("Sample")
	bestword=BranchAndBoundMedianSearch(DNA, t, n, l)
	print("Branch And Bound Median Search:")
	print("Best Word:", bestword, sep=" ")

	return 0

if __name__ == "__main__":
	sys.exit(int(main() or 0))
