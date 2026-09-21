#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    int estado_salida;
    FILE *archivo;
    int byte_actual;
    int num_aleatorio;
    time_t tiempo_actual;

    if (argc < 2) {
        printf("Usage: sumnotransfer <archivo>\n");
        estado_salida = 1;
    }
    else {

        tiempo_actual = time(NULL);
        srand((unsigned int)tiempo_actual);

        archivo = fopen(argv[1], "rb");

        if (archivo == NULL) {
            printf("No se puede abrir el archivo \n");
            estado_salida = 1;
        }
        else {

            do {
                byte_actual = fgetc(archivo);

                if (byte_actual != EOF) {
                     num_aleatorio = rand() % 256;

                     if (byte_actual < num_aleatorio) {
                         printf("%d-%d\n", num_aleatorio, num_aleatorio - byte_actual);
                     }

                     if (num_aleatorio < byte_actual) {
                         printf("%d+%d\n", byte_actual - num_aleatorio, num_aleatorio);
                     }

                     if (byte_actual == 0) {
                         printf("[NULL]\n");
                     }

                     if (num_aleatorio == byte_actual) {
                         printf("%d+1\n", byte_actual - 1);
                     }

                }
            } while (byte_actual != EOF);

            fclose(archivo);
            estado_salida = 0;
        }
    }
    return estado_salida;
}
