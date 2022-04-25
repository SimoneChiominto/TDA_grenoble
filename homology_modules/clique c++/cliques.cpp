// C++ implementation of the approach
#include <iostream>
#include <fstream>
#include <bits/stdc++.h>
using namespace std;
int ** import_matrix(char* file_name, int n_row, int n_col);
void findCliques(int i, int l, int s,int**M, int *store , int *d,FILE* file);


void print_matrix(int **M){
  for(int i=0; i<90; i++){
    for (int j=0; j<90; j++){
      printf("%d", M[i][j]);
    }
    printf("\n");
  }
}

void print_vector(int *v, int len){
  for(int i=0; i<len; i++){
    printf("%d ", v[i]);
  }
  printf("\n");
}
// Function to check if the given set of vertices
// in store array is a clique or not
bool is_clique(int b, int** graph, int* store)
{
	// Run a loop for all the set of edges
	// for the select vertex
  //print_vector(store,4);
	for (int i = 0; i <= b; i++) {
		for (int j = i + 1; j <= b; j++)

			// If any edge is missing
			if (graph[store[i]][store[j]] < 1)
				return false;
	}
	return true;
}


void findCliques_appo(int i, int l, int s,char* file_name ){

  FILE *myfile;
  myfile=fopen("cliques.txt","w");
  int n=90;
  int *store=new int[n];
  int *d= new int[n];
  int **M= import_matrix(file_name,90,90);

  findCliques(i,l,s-1,M,store,d,myfile );
  fclose(myfile);
}



// Function to find all the cliques of size s
void findCliques(int i, int l, int s,int**M, int *store , int *d, FILE* file)
{
  //printf("sono entrato %d ", l);
  int n=90;
    //ofstream myfile;
    //	myfile.open ("cliques.txt");
 	// Check if any vertices from i+1 can be inserted
  //for (int j = i + 1; j <= n - (s - l); j++){
    for (int j = i ; j < n ; j++){
    //printf("sono entrato nel primo for %d", j);

		// If the degree of the graph is sufficient
		//if (d[j] >= s - 1) {
 

			// Add the vertex to store
			store[l] = j;
			//printf("%d ", store[l]);

			// If the graph is not a clique of size k
			// then it cannot be a clique
			// by adding another edge
			if (is_clique(l , M, store)){
			  //printf("\n isclique!!  \n");
				// If the length of the clique is
				// still less than the desired size
			  if (l < s){

					// Recursion to add vertices
				  findCliques(j, l + 1, s, M, store, d,file);
			  }
				// Size is met
				
				  //printf("sono arrivato dove si stampaaa");
				  // Function to print the clique
				  /*	for (int ii = 1; ii < l+1; ii++)
					  	  myfile << store[ii] << " ";
					myfile << ", ";}
				  */
			  for( int ii=0; ii<=l; ii++)
			    {
			      fprintf( file, "%d", store[ii]);
			      if (ii!=l)
				fprintf(file, ",");
			    }
			  fprintf(file,"\n");

			}
			//myfile.close();
		     
				}

}




int ** import_matrix(char* file_name, int n_row, int n_col){

  ifstream is(file_name);
  

  int **M = new int *[n_col];
  for (int j=0;j<n_col; j++)
    {M[j] = new int [n_row];}
  
  is.seekg(0,ios::beg);
    for (int i=0;i!=n_row;i++)
        {
        for (int j=0;j!=n_col;j++)
	  {
            double temp;
            is>>temp;
            M[i][j]=int(temp);
	  }
        is.ignore(1000000,'\n');
	}
    is.close();
    return M;


}


/*int main(){
  findCliques_appo( 0, 0, 3,"data1.csv" );
}
*/

// Driver code

extern "C"{
  int FindCliques(int a, int b, int c, wchar_t* file_name)
	{
	  //printf("ciaoooo");
	  char *filename1= (char *)malloc( 50);
	  wcstombs( filename1,file_name, 50);
	  findCliques_appo(a,b,c, filename1);
	  return 0;
	}
}
