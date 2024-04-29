from Readers.Lector_yalex import *   
from Readers.Lector_yapar import *
# ---------------------LECTURA DE YALEX ----------------------------

yalex = "yalex/prueba.yal"
yapar = "yapar/prueba.yalp"

symbols = read_var(yalex)

print("Símbolos leídos del archivo")
print (symbols)


read_regdef(yalex)

regular_dict = convert_to_dictionary(regular_elements)

print("Regdef leído del archivo")
print (regular_dict)

# ---------------------LECTURA DE YAPAR ----------------------------
tokens, result = read_tokens(yapar, regular_dict)
print(tokens)
print(result)

if result == True:
    print("Error en la lectura de tokens")
    exit()
