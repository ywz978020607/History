
void show_matrix(int *matrix, int rows, int columns)
{
    int i, j;
    for (i=0; i<rows; i++) {
        for (j=0; j<columns; j++) {
            printf("matrix[%d][%d] = %d\n", i, j, matrix[i*rows + j]);
        }
    }
}