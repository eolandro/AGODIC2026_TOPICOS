#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[])
{
    int iVar1;
    FILE *_File;
    int iVar2;
    time_t tVar3;

    if (argc < 2)
    {
        printf("Usage:\nsumnotransfer archivo");
        iVar1 = 1;
    }
    else
    {
        tVar3 = time((time_t *)0);
        srand((unsigned int)tVar3);

        _File = fopen(argv[1], "rb");
        if (_File == NULL)
        {
            printf("No se puede abrir el archivo");
            iVar1 = 1;
        }
        else
        {
            do
            {
                iVar1 = fgetc(_File);
                if (iVar1 != -1)
                {
                    iVar2 = rand();
                    iVar2 = iVar2 % 0x100;

                    if (iVar1 < iVar2)
                    {
                        printf("%d-%d\n", iVar2, iVar2 - iVar1);
                    }
                    if (iVar2 < iVar1)
                    {
                        printf("%d+%d\n", iVar1 - iVar2, iVar2);
                    }
                    if (iVar1 == 0)
                    {
                        printf("1-1\n");
                    }
                    if (iVar2 == iVar1)
                    {
                        printf("%d+1\n", iVar1 - 1);
                    }
                }
            } while (iVar1 != -1);

            fclose(_File);
            iVar1 = 0;
        }
    }

    return iVar1;
}
