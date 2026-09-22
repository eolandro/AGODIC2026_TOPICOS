/*
 R003 - Reconstruccion del codigo fuente
 Ejecutable analizado: desconocido.exe
 Herramienta: Ghidra / Decompiler
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[])
{
    FILE *archivo;
    int byteLeido;
    int valorAleatorio;
    time_t semilla;

    if (argc < 2)
    {
        printf("Usage: sumnotransfer archivo\n");
        return 1;
    }

    semilla = time(NULL);
    srand((unsigned int)semilla);

    archivo = fopen(argv[1], "rb");

    if (archivo == NULL)
    {
        printf("No se puede abrir el archivo\n");
        return 1;
    }

    do
    {
        byteLeido = fgetc(archivo);

        if (byteLeido != EOF)
        {
            valorAleatorio = rand() % 256;

            if (byteLeido < valorAleatorio)
            {
                printf("%d-%d\n",
                       valorAleatorio,
                       valorAleatorio - byteLeido);
            }

            if (valorAleatorio < byteLeido)
            {
                printf("%d+%d\n",
                       byteLeido - valorAleatorio,
                       valorAleatorio);
            }

            if (byteLeido == 0)
            {
                printf("1-1\n");
            }

            if (valorAleatorio == byteLeido)
            {
                printf("%d+1\n", byteLeido - 1);
            }
        }

    } while (byteLeido != EOF);

    fclose(archivo);
    return 0;
}
