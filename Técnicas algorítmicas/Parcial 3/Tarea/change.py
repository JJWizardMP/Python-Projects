import sys
import numpy

def CheckArgs():
	flag=False; change=0; x=[]; C=[];
	if (len(sys.argv) >= 3):
		x=sys.argv[1].split(',')
		C=list(map(int, x))
		change=int(sys.argv[2])
		flag=True
	else:
		print("Two arguments are necessary!")
		print("First Argument: An array that contains the coins for change | Format should be like 1,2,3,4,...,3")
		print("Second Argument: Change to return | A int value")
	return (C,change,flag)

def DPChange(change, c, d): #Book Chapter 6.2
	used=[0]*(change+1)
	bestNumCoins = [0]
	for m in range(change+1):
		bestNumCoins.append(10000)
		newcoin=1
		for i in range(d):
			if m >= c[i]:
				if bestNumCoins[m- c[i]] + 1 < bestNumCoins[m]: 
					bestNumCoins[m]= bestNumCoins[m - c[i]]+ 1
					newcoin=c[i]
		used[m]=newcoin
	PrintCoins(getCoins(used, change))

def DPchange(C,change,minCoins,usedCoins): #Internet: http://interactivepython.org/runestone/static/pythoned/Recursion/ProgramacionDinamica.html | Programa 8
	for cen in range(change+1):
		countcoins = cen
		newcoin = 1
		for j in [m for m in C if m <= cen]:
			if minCoins[cen-j] + 1 < countcoins:
				countcoins = minCoins[cen-j]+1
				newcoin = j
		minCoins[cen] = countcoins
		usedCoins[cen] = newcoin
	#Get Vector
	PrintCoins(getCoins(usedCoins, change))

def getCoins(usedCoins,change):
	CC=[]
	coin = change
	while coin > 0:
		thiscoin= usedCoins[coin]
		CC.append(thiscoin)
		coin = coin - thiscoin
	return (CC) 

def PrintCoins(VectorC):
	Uniq=list(numpy.unique(VectorC))
	Uniq.reverse()
	for i in Uniq:
		c=VectorC.count(i)
		if(c > 1):
			print(c, "Monedas de", i, sep=" ")	
		else:
			print(c, "Moneda de", i, sep=" ")	

def main():
	C=[]
	change=0
	#Read Arguments of the Command Line:
	#C,change,flag=CheckArgs() #//#
	#Set Normal Values:
	C=[1,5,10,20,25,50]
	change=40; flag=True #//#
	minCoins=[0]*(change+1)
	usedCoins=[0]*(change+1)
	if(flag):
		print("Coins: ", C, sep=" ")
		print("Change: ", change, sep=" ")
		print("\nCode from Book: ")
		DPChange(change,C,len(C))
		print("Code from Internet: ")
		DPchange(C,change,minCoins,usedCoins)
	return 0

if __name__ == "__main__":
	sys.exit(int(main() or 0))
