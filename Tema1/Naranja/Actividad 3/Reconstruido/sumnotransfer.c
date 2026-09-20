#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char **argv)
{
    int resultado;
    int c;
    int r;
    time_t semilla;
    FILE *f;

    if (argc < 2) {
        printf("Usage:\nsumnotransfer archivont");
        resultado = 1;
    }
    else {
        semilla = time(0);
        srand((unsigned int)semilla);
        f = fopen(argv[1], "rb");
        if (f == NULL) {
            printf("No se puede abrir el archivont\n");
            resultado = 1;
        }
        else {
            do {
                c = fgetc(f);
                if (c != -1) {
                    r = rand();
                    r = r % 256;
                    if (c < r) {
                        printf("%d-%d\n", r, r - c);
                    }
                    if (r < c) {
                        printf("%d+%d\n", c - r, r);
                    }
                    if (c == 0) {
                        printf("1-1\n");
                    }
                    if (r == c) {
                        printf("%d+1\n", c - 1);
                    }
                }
            } while (c != -1);
            fclose(f);
            resultado = 0;
        }
    }

    return resultado;
}