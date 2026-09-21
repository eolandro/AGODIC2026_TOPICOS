#include <stdio.h>

int main(void)
{
    int i;
    int suma = 0;
    FILE *archivo;

    for (i = 1; i <= 5; i++)
    {
        suma = suma + i;
    }

    archivo = fopen("resultado.json", "w");

    if (archivo == NULL)
    {
        return 1;
    }

    fprintf(archivo,
        "{\n"
        "  \"materia\": \"Topicos de Ciberseguridad\",\n"
        "  \"valor\": %d,\n"
        "  \"estado\": \"activo\"\n"
        "}\n",
        suma
    );

    fclose(archivo);

    return 0;
}