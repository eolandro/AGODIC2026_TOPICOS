#include <stdio.h>

int main(void)
{
    int i;
    int suma = 0;
    FILE *archivo;

    for (i = 1; i < 6; i++)
    {
        suma = suma + i;
    }

    archivo = fopen("resultado.json", "w");

    if (archivo != NULL)
    {
        fprintf(
            archivo,
            "{\n"
            "  \"materia\": \"Topicos de Ciberseguridad\",\n"
            "  \"valor\": %d,\n"
            "  \"estado\": \"activo\"\n"
            "}\n",
            suma
        );

        fclose(archivo);
    }

    return archivo == NULL;
}