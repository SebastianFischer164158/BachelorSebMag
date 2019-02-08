#include<stdio.h>
#define LEN(arr) ((int) (sizeof (arr) / sizeof (arr)[0]))
int main(){
   /* 2D array declaration*/
   int disp[2][4] = {
    {10, 11, 12, 13},
    {14, 15, 16, 17}
};
   int row_count = LEN(disp);
   int column_count = LEN(disp[0]);
   
   printf("Number of rows: %d\n", LEN(disp));
   printf("Number of columns: %d\n", LEN(disp[0]));
   //Displaying array elements
   int i,j;
   printf("Two Dimensional array elements:\n");
   for(i=0; i<row_count; i++) {
      for(j=0;j<column_count; j++) {
         printf("%d ", disp[i][j]);
         if(j==column_count-1){
            printf("\n");
         }
      }
   }
   
   return 0;
}
