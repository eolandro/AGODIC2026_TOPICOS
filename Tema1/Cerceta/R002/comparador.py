with open("T.exe", "rb") as original, open("parche_T.exe", "rb") as parche:
    original = original.read()
    parchado = parche.read()

for i in range(min(len(original), len(parchado))):
    if original[i] != parchado[i]:
        print(f"Offset {hex(i)}: {original[i]:02X} -> {parchado[i]:02X}")
        
        
        
        
        
       # EN ESTA PARTE SE SUPONE QUE SE COMPARAN LOS VALORES HEXADECIMALES DE EL PARCHE Y EL ORIGINAL}
        #ME DARA LA POSICIOIN QUE ES DIFERENTE