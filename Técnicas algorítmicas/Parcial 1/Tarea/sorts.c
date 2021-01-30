/*Programa en C para calcular los tiempos en segundos de los algoritmos de métodos de ordenación.
Descripcion: Implementar Insertion Sort, Merge Sort, Bubble Sort en C para leer y ordenar conjuntos de números de archivos externos.
Programador: Joan de Jesús Méndez Pool
Fecha de creacion: 24/08/2018 | Versión Mejorada(29/03/2019)
Entradas: 3 archivos externos (n100.txt, n1000.txt , n10000.txt)
Salida: Tabla comparativa del tiempo de ejecución de los métodos de ordenación(Insertion, Merge, Bubble) para 100, 1000 y 10000 números usando segundos como unidad de tiempo
*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void control( double **, char **name);
void exe_time(double **, char **);
void create_files(char **name);
void delete_files(char **name);
void interaction(int *, int);
void set_names(char **, char **);
void filerand(char *, int, int);
int countfile(char *);
int *readfile(char *, int);
double **set_timevar();
//Sorts
void insertion_sort(int *, int);
void merge_sort(int *, int, int);
void merge(int *, int, int, int);
void bubble_sort(int *, int);

void kill(int **);
void killdb(double **, int );

const int INF=999999;
int main(){
	char **name=(char**)calloc(3, sizeof(char*)), **sort=(char**)calloc(3, sizeof(char*));
	double **total_time=NULL;	
	time_t t;
	srand((unsigned) time(&t));

	total_time=set_timevar();
	set_names(name, sort);
	create_files(name);
	control(total_time, name);
	exe_time(total_time, sort);
	delete_files(name);

	killdb(total_time, 3);
	printf("\n\n");
	return 0;
}

void control(double **total_time, char **name){
	clock_t start[3][3], end[3][3];	
	int *A=NULL;
	int j=0, n=0;
	for(int i=0; i<3; i++){
		//Insertion Sort
		n=countfile(name[i]);
		A=readfile(name[i], n);
		start[0][j] = clock();

		insertion_sort(A, n); 

		end[0][j] = clock();
		total_time[0][j] = ((double) (end[0][j] - start[0][j])) / CLOCKS_PER_SEC;//calulate total time
		kill(&A);

		//Merge Sort
		n=countfile(name[i]);
		A=readfile(name[i], n);
		start[1][j] = clock();

		merge_sort(A, 1, n);

		end[1][j] = clock();
		total_time[1][j] = ((double) (end[1][j] - start[1][j])) / CLOCKS_PER_SEC;//calulate total time
		kill(&A);

		//Bubble Sort
		n=countfile(name[i]);
		A=readfile(name[i], n);
		start[2][j] = clock();

		bubble_sort(A, n);

		end[2][j] = clock();
		total_time[2][j] = ((double) (end[2][j] - start[2][j])) / CLOCKS_PER_SEC;//calulate total time
		j++;
		kill(&A);
	}
}
void exe_time(double **total_time, char **sort){
	printf("\nFor\t\t100n\t\t1,000n\t\t10,000n\n\n");
	for(int i=0; i<3; i++){
		printf("%s\t", sort[i]);
		for(int j=0; j<3; j++){
			if(j==2){
				printf("%f\n", total_time[i][j]);
			}else{
				printf("%f\t", total_time[i][j]);
			}
		}
	}
}
void create_files(char **name){
	int m=100;
	int r=25000;
	for(int i=0; i<3; i++){
		filerand(name[i], m, r);
		m*=10;
	}
}
void delete_files(char **name){
	for(int i=0; i<3; i++){
		remove(name[i]);
	}
}
void interaction(int *ptr, int N){
	if(ptr!=NULL){
		for(int i=0; i<N; i++){
			if(i==N-1){
				printf("%d", ptr[i]);
			}else{
				printf("%d, ", ptr[i]);
			}
		}
	}else{
		printf("\nEmpty!\n");
	}
}
double **set_timevar(){
	double **time=(double**)calloc(3, sizeof(double*));
	for(int i=0; i<3; i++){
		time[i]=(double*) calloc(3, sizeof(double));
	}
	return time;
}
void set_names(char **name, char **sort){
	name[0]="n100.txt";
	name[1]="n1000.txt";
	name[2]="n10000.txt";
	sort[0]="Insertion Sort";
	sort[1]="Merge Sort";
	sort[2]="Bubble Sort";
}
void filerand(char *handle, int n, int r){
	FILE *api=fopen(handle, "w");
	int cad=0;
	for(int i=0; i<n; i++){
		cad=rand()%r+1;
		if(i==n-1){
			fprintf(api,"%d%c", cad, EOF);
		}else{
			fprintf(api,"%d\n", cad);
		}
	}
	fclose(api);
}
int countfile(char *handle){
	FILE *api=fopen(handle, "r");
	int id=0;
	char p1;

	if(api != NULL){
		while ((p1 = fgetc(api)) != EOF){
			if(p1=='\n'){
				id++;
			}
		}
		fclose(api);
	}
	return ++id;
}
int *readfile(char *handle, int n){
	char line[10];
	int *ptr=(int*)calloc(n, sizeof(int));
	int id=0;
	FILE *api= fopen(handle, "r");

	while(fgets(line, 10, (FILE*) api)) {
		ptr[id++]=atoi(line);
	}
	fclose(api);
	return ptr;
}
//Sorts
void insertion_sort(int *A, int n){
	int key=0, i=0; 
	for(int j=1; j<n; j++){
		key=A[j];
		i=j-1;
		while((i>=0)&&(key<A[i])){
			A[i+1]=A[i];
			i--;
		}
		A[i+1]=key;
	}
}
void merge_sort(int *A, int p, int r){
	int q=0;
	if(p<r){
		q=((p+r)/2);
		merge_sort(A, p, q);
		merge_sort(A, q+1, r);
		merge(A, p, q, r);
	}
}
void merge(int *A, int p, int q, int r){
	int n1=q-p+1, n2=r-q;
	int *L=(int*)calloc(n1+1, sizeof(int)), *R=(int*)calloc(n2+1, sizeof(int));	
	int i=0, j=0;

	for(i=1; i<=n1; i++){
		L[i-1]=A[p+i-2];
	}
	for(j=1; j<=n2; j++){
		R[j-1]=A[q+j-1];
	}
	L[n1]=INF, R[n2]=INF;
	i=0, j=0;
	for(int k=p-1; k<r; k++){
		if(L[i]<=R[j]){
			A[k]=L[i++];
		}else{
			A[k]=R[j++];
		}
	}
	kill(&L);
	kill(&R);
}
void bubble_sort(int *A, int n ){
	int key=0;
	for(int i=0; i<n; i++){
		for(int j=n-1; j>=i+1; j--){
			if(A[j]<A[j-1]){
				key=A[j];	
				A[j]=A[j-1];
				A[j-1]=key;
			}
		}
	}
}
void kill(int **ptr){
	if(ptr[0]!=NULL){
		free(*ptr);
		*ptr=NULL;
	}
}
void killdb(double **matriz, int N){
	if(matriz[0]!=NULL){
		for(int i=0; i<N; i++){
			free(matriz[i]);
			matriz[i]=NULL;
		}
		free(matriz);
		matriz=NULL;
	}	
}
