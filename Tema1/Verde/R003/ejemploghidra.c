
bool FUN_00401000(void)

{
  FILE *_File;
  
  _File = fopen(s_resultado.json_00402000,&DAT_0040200f);
  if (_File != (FILE *)0x0) {
    fprintf(_File,&DAT_00402032);
    fprintf(_File,s_"equipo":_"Equipo_Verde",_00402035);
    fprintf(_File,s_"nom-integrantes":_"mafer,_mich,_00402052);
    fprintf(_File,s_"estado":_"Exitoso"_0040207f);
    fprintf(_File,&DAT_00402096);
    fclose(_File);
    printf(&DAT_00402099);
  }
  else {
    printf(s_Error_al_crear_el_archivo_JSON._00402011);
  }
  return _File == (FILE *)0x0;
}
