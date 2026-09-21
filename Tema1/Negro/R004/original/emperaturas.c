#include <stdio.h>

#define NUM_DIAS 7
#define UMBRAL_ALERTA 30.0

typedef struct {
    float minimo;
    float maximo;
    float promedio;
    int dias_alerta;
} Estadisticas;

static float lecturas[NUM_DIAS] = {
    22.5f, 25.0f, 31.2f, 28.7f, 33.1f, 19.8f, 27.4f
};

const char *dia_nombre(int indice) {
    static const char *nombres[NUM_DIAS] = {
        "Lunes", "Martes", "Miercoles", "Jueves",
        "Viernes", "Sabado", "Domingo"
    };
    if (indice < 0 || indice >= NUM_DIAS) {
        return "Desconocido";
    }
    return nombres[indice];
}

Estadisticas calcular_estadisticas(float datos[], int n) {
    Estadisticas resultado;
    float suma = 0.0f;
    int i;

    resultado.minimo = datos[0];
    resultado.maximo = datos[0];
    resultado.dias_alerta = 0;

    for (i = 0; i < n; i++) {
        float valor = datos[i];

        if (valor < resultado.minimo) {
            resultado.minimo = valor;
        }
        if (valor > resultado.maximo) {
            resultado.maximo = valor;
        }
        if (valor >= UMBRAL_ALERTA) {
            resultado.dias_alerta = resultado.dias_alerta + 1;
        }

        suma = suma + valor;
    }

    resultado.promedio = suma / (float)n;
    return resultado;
}

int escribir_reporte_json(const char *ruta, Estadisticas stats, float datos[], int n) {
    FILE *archivo;
    int i;

    archivo = fopen(ruta, "w");
    if (archivo == NULL) {
        printf("Error: no se pudo crear el archivo %s\n", ruta);
        return 1;
    }

    fprintf(archivo, "{\n");
    fprintf(archivo, "  \"estacion\": \"Central\",\n");
    fprintf(archivo, "  \"lecturas\": [\n");

    for (i = 0; i < n; i++) {
        fprintf(archivo, "    { \"dia\": \"%s\", \"temperatura\": %.1f }",
                dia_nombre(i), datos[i]);
        if (i < n - 1) {
            fprintf(archivo, ",");
        }
        fprintf(archivo, "\n");
    }

    fprintf(archivo, "  ],\n");
    fprintf(archivo, "  \"estadisticas\": {\n");
    fprintf(archivo, "    \"minimo\": %.1f,\n", stats.minimo);
    fprintf(archivo, "    \"maximo\": %.1f,\n", stats.maximo);
    fprintf(archivo, "    \"promedio\": %.2f,\n", stats.promedio);
    fprintf(archivo, "    \"dias_alerta_calor\": %d\n", stats.dias_alerta);
    fprintf(archivo, "  }\n");
    fprintf(archivo, "}\n");

    fclose(archivo);
    return 0;
}

int main(void) {
    Estadisticas stats;
    int resultado;

    printf("Generando reporte de temperaturas...\n");

    stats = calcular_estadisticas(lecturas, NUM_DIAS);
    resultado = escribir_reporte_json("reporte.json", stats, lecturas, NUM_DIAS);

    if (resultado == 0) {
        printf("Reporte generado exitosamente en reporte.json\n");
        printf("Minimo: %.1f, Maximo: %.1f, Promedio: %.2f, Dias de alerta: %d\n",
               stats.minimo, stats.maximo, stats.promedio, stats.dias_alerta);
    }

    return resultado;
}
