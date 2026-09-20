#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *archivo = fopen("resultado.json", "w");
    
    if (archivo == NULL) {
        printf("Error al crear el archivo JSON.\n");
        return 1;
    }

    fprintf(archivo, "{\n");
    fprintf(archivo, "  \"equipo\": \"Equipo Verde\",\n");
    fprintf(archivo, "  \"nom-integrantes\": \"mafer, mich, anibal\",\n");
    fprintf(archivo, "  \"estado\": \"Exitoso\"\n");
    fprintf(archivo, "}\n");

    fclose(archivo);

    printf("¡Archivo JSON generado con exito!\n");
    return 0;
}
