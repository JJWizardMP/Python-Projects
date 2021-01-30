#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void create_files(char **name);
void delete_files(char **name);
void interaction(int *, int);
void set_names(char **, char **);
void filerand(char *, int, int);
int countfile(char *);
int *readfile(char *, int);
//Quick Sort
void quick_sort(int *, int, int);
int partition(int *, int, int);
int randomized_partition(int *, int , int );
void kill(int **);

int main(){
	int m=0;
	int *A=NULL;
	char **name=(char**)calloc(3, sizeof(char*)), **sort=(char**)calloc(3, sizeof(char*));
	double **total_time=NULL;	
	time_t t;
	srand((unsigned) time(&t));

	set_names(name, sort);
	create_files(name);
	m=countfile(name[1]);
	A=readfile(name[1], m);
	//interaction(A, m);
	quick_sort(A,0, m-1);
	interaction(A, m);
	delete_files(name);

	printf("\n\n");
	return 0;
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
		for(int i=1; i<N; i++){
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
void quick_sort(int *A, int p, int r){
	int q=0;
	if(p<r){
		q=randomized_partition(A, p, r);
		quick_sort(A, p, q-1);
		quick_sort(A, q+1, r);
		
	}
}
int partition(int *A, int p, int r){
	int x=A[r], i=p-1;
	int key=0;
	for(int j=p; j<=r-1; j++){
		if(A[j]<=x){
			i++;
			key=A[i];
			A[i]=A[j];
			A[j]=key;
		}
	}
	key=A[i+1];
	A[i+1]=A[r];
	A[r]=key;

	return i+1;	
}
int randomized_partition(int *A, int p, int r){
	int i=p + (rand() % (r-p));
	int key=0;
	key=A[r];
	A[r]=A[i];
	A[i]=key;

	return partition(A,p,r);
}

void kill(int **ptr){
	if(ptr[0]!=NULL){
		free(*ptr);
		*ptr=NULL;
	}
}
