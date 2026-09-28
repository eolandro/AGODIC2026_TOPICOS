#include <stdio.h>

int main(void) {
    FILE *_File;
    _File = fopen("archivo.json", "w");
    if (_File != NULL) {
        fprintf(_File, "{\"mensaje\": \"Hola_a_todos\"}");
        fclose(_File);
    }
    return 0;
}
