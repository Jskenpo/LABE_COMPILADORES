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


# ---------------------LECTURA DE YAPAR ----------------------------
tokens, result = read_tokens(yapar, regular_dict)

if result == True:
    print("Error en la lectura de tokens")
    exit()

productions, separador = read_productions(yapar)

if separador == True:
    print("Error en la lectura de producciones")
    exit()

# ---------------------GRAMATICA ARGUMENTADA ----------------------------

new_grammar = generar_gramatica_argumentada(productions)
print("Gramática argumentada\n")
print(new_grammar)
print ("\n")

# ---------------------AUTOMATA----------------------------

automata = elementosLR0(new_grammar)

# ---------------------FIRST Y FOLLOW----------------------------

# Ejemplo de uso
non_terminals = non_terminals(new_grammar)


terminals = terminals(new_grammar, non_terminals)




first_set = compute_first(new_grammar, non_terminals, terminals)
follow_set = compute_follow(new_grammar, non_terminals, new_grammar[0][0], first_set)


print("FIRST sets:")
for non_terminal in non_terminals:
    print(f"FIRST({non_terminal}) = {first_set[non_terminal]}")


print("\nFOLLOW sets:")
for non_terminal in non_terminals:
    print(f"FOLLOW({non_terminal}) = {follow_set[non_terminal]}")

    # Construir conjuntos LR(1)
conjuntos_lr1 = construir_conjuntos_lr1(automata, new_grammar, first_set, follow_set, non_terminals)

# Construir action table y goto table
action_table, goto_table = construir_tabla_slr(automata, new_grammar, conjuntos_lr1)

# Imprimir las tablas (o cualquier otra operación que desees realizar con ellas)
print("Action Table:")
for estado, acciones in action_table.items():
    print(f"{estado.name}: {acciones}")

print("\nGoto Table:")
for estado, transiciones in goto_table.items():
    print(f"{estado.name}: {transiciones}")