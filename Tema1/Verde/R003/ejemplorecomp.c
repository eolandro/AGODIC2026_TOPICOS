
#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *archivo = fopen("resultado.json", "w");
    
    if (archivo != NULL) {
        fprintf(archivo, "{\n");
        fprintf(archivo, "  \"equipo\": \"Equipo_Verde\",\n");
        fprintf(archivo, "  \"nom-integrantes\": \"mafer, mich\",\n");
        fprintf(archivo, "  \"estado\": \"Exitoso\"\n");
        fprintf(archivo, "}\n");
        
        fclose(archivo);
        
        return 0;
    } else {
        printf("Error al crear el archivo JSON.\n");
        return 1;
    }
}