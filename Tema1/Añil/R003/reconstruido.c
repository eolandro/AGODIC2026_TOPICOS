#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[])
{
    FILE *archivo;
    int letra;
    int numero;

    if (argc < 2)
    {
        printf("Usage:\nsumnotransfer archivo\n");
        return 1;
    }
    archivo = fopen(argv[1], "rb");
    if (archivo == NULL)
    {
        printf("No se puede abrir el archivo\n");
        return 1;
    }
    srand(time(NULL));
    while ((letra = fgetc(archivo)) != -1)
    {
        numero = rand() % 256;
        if (letra < numero)
            printf("%d-%d\n", numero, numero - letra);
        if (numero < letra)
            printf("%d+%d\n", letra, letra - numero);
        if (letra == 0)
            printf("1-1\n");
        if (numero == letra)
            printf("%d+1\n", letra + 1);
    }
    fclose(archivo);
    return 0;
}
