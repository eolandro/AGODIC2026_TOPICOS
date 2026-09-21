import sys
import random

def tradCaPy():
    if len(sys.argv) < 2:
        print("Se usa con la sintaxis: python traduccionCaPy.py <archivo>")
        sys.exit(1)
        
    nombre_archivo = sys.argv[1]
    
    try:

        with open(nombre_archivo, 'rb') as file:
          
            while True:
                byte_data = file.read(1)
                
                if not byte_data:
                    break
                    
                iVar2 = ord(byte_data)    
                iVar3 = random.randint(0, 255)
                

                if iVar2 < iVar3:
                    print(f"{iVar3}-{iVar3 - iVar2}")
                    
                if iVar3 < iVar2:
                    print(f"{iVar2 - iVar3}+{iVar3}")
                    
                if iVar2 == 0:
                    print("0")
                    
                if iVar3 == iVar2:
                    print(f"{iVar2 - 1}+1")

        print()
        sys.exit(0)

    except FileNotFoundError:
        print(f"No se puede abrir el archivo")
        sys.exit(1)
    except PermissionError:
        print(f"Permiso denegado para abrir el archivo")
        sys.exit(1)

if __name__ == "__main__":
    tradCaPy()


''' ###########################################################                
              código de C traducido a Python

undefined4 __cdecl FUN_00401000(int param_1,int param_2)

{
  undefined4 uVar1;
  FILE *_File;
  int iVar2;
  int iVar3;
  time_t tVar4;
  
  if (param_1 < 2) {
    printf(s_Usage:_sumnotransfer_archivont_00402000);
    uVar1 = 1;
  }
  else {
    tVar4 = time((time_t *)0x0);
    srand((uint)tVar4);
    _File = fopen(*(char **)(param_2 + 4),&DAT_0040201f);
    if (_File == (FILE *)0x0) {
      printf(s_No_se_puede_abrir_el_archivont_00402022,0);
      uVar1 = 1;
    }
    else {
      do {
        iVar2 = fgetc(_File);
        if (iVar2 != -1) {
          iVar3 = rand();
          iVar3 = iVar3 % 0x100;
          if (iVar2 < iVar3) {
            printf(s_%d-%d_00402042,iVar3,iVar3 - iVar2);
          }
          if (iVar3 < iVar2) {
            printf(s_%d+%d_00402049,iVar2 - iVar3,iVar3);
          }
          if (iVar2 == 0) {
            printf(&DAT_00402050);
          }
          if (iVar3 == iVar2) {
            printf(s_%d+1_00402055,iVar2 + -1);
          }
        }
      } while (iVar2 != -1);
      fclose(_File);
      uVar1 = 0;
    }
  }
  return uVar1;
}
'''