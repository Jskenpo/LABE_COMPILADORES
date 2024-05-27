from Readers.Lector_yalex import *   
from Readers.Lector_yapar import *
from prepare import *
from Automata import *
from TablaSLR import *
# ---------------------LECTURA DE YALEX ----------------------------

yalex = "yalex/prueba.yal"
yapar = "yapar/prueba.yalp"

symbols = read_var(yalex)

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

productions, separador = read_productions(yapar)
print("Producciones leídas del archivo")
print (productions)

if separador == True:
    print("Error en la lectura de producciones")
    exit()

# ---------------------GRAMATICA ARGUMENTADA ----------------------------

new_gramar = generar_gramatica_argumentada(productions)
print("Gramática argumentada")
print(new_gramar)

# ---------------------AUTOMATA----------------------------

automata = elementosLR0(new_gramar)

# ---------------------FIRST Y FOLLOW----------------------------

# Ejemplo de uso
non_terminals = non_terminals(new_gramar)
print("No terminales")
print(non_terminals)

terminals = terminals(new_gramar, non_terminals)


print("Terminales")
print(terminals)

first = compute_first(new_gramar, non_terminals, terminals, new_gramar)
follow = compute_follow(new_gramar, non_terminals, terminals, first)

print("FIRST:")
for non_terminal, first_set in first.items():
    if non_terminal in non_terminals:
        print(f"{non_terminal}: {', '.join(first_set)}")

print("\nFOLLOW:")
for non_terminal, follow_set in follow.items():
    if non_terminal in non_terminals:
        print(f"{non_terminal}: {', '.join(follow_set)}")