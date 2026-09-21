# include <stdio.h>
int valido = 0;
int main (int argc, char **argv){
    if (valido == 127){
        printf("Acceso Consedido");
    }else{
        printf("Acceso Denegado");
    }
    return 0;
}
// tcc.exe ..\..\hackame0.c -o ejemplo.exe
