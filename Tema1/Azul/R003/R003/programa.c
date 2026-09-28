#include <stdio.h>

int main() {
    FILE *archivo = fopen("archivo.json", "w");
    if (archivo == NULL) {
        return 1;
    }
    fprintf(archivo, "{\"mensaje\": \"Hola a todos\"}");
    fclose(archivo);
    return 0;
}
