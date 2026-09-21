#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int param_1, char **param_2)
{
    int uVar1;
    FILE *_File;
    int iVar2;
    int iVar3;
    time_t tVar4;
    
    if (param_1 < 2) {
        printf("Usage: sumnotransfer archivo.txt\n");
        uVar1 = 1;
    }
    else {
        tVar4 = time((time_t *)0x0);
        srand((unsigned int)tVar4);
        _File = fopen(param_2[1], "rb");
        if (_File == (FILE *)0x0) {
            printf("No se puede abrir el archivo\n");
            uVar1 = 1;
        }
        else {
            do {
                iVar2 = fgetc(_File);
                if (iVar2 != -1) {
                    iVar3 = rand();
                    iVar3 = iVar3 % 0x100;
                    if (iVar2 < iVar3) {
                        printf("%d-%d\n", iVar3, iVar3 - iVar2);
                    }
                    if (iVar3 < iVar2) {
                        printf("%d+%d\n", iVar2 - iVar3, iVar3);
                    }
                    if (iVar2 == 0) {
                        printf("\n");
                    }
                    if (iVar3 == iVar2) {
                        printf("%d+1\n", iVar2 - 1);
                    }
                }
            } while (iVar2 != -1);
            fclose(_File);
            uVar1 = 0;
        }
    }
    return uVar1;
}