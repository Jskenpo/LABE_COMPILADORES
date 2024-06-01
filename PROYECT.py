from Readers.Lector_yalex import *   
from Readers.Lector_yapar import *
from prepare import *
from Automata import *
from TablaSLR import *
from Parser import *
# ---------------------LECTURA DE YALEX ----------------------------

yalex = "yalex/prueba.yal"
yapar = "yapar/rr.yalp"

symbols = read_var(yalex)

read_regdef(yalex)

regular_dict = convert_to_dictionary(regular_elements)


# ---------------------LECTURA DE YAPAR ----------------------------
tokens, result = read_tokens(yapar, regular_dict)

'''if result == True:
    print("Error en la lectura de tokens")
    exit()
'''
productions, separador = read_productions(yapar)

if separador == True:
    print("Error en la lectura de producciones")
    exit()

# ---------------------GRAMATICA ARGUMENTADA ----------------------------

new_grammar = generar_gramatica_argumentada(productions)
gramatica = new_grammar
print("Gramática aumentada\n")
print(new_grammar)
print ("\n")

# ---------------------AUTOMATA----------------------------

automata = elementosLR0(new_grammar)

# ---------------------FIRST Y FOLLOW----------------------------

# Ejemplo de uso
non_terminals = non_terminals(new_grammar)
print("No terminales: ", non_terminals)

terminals = terminals(new_grammar, non_terminals)
# Agregar el símbolo de fin de entrada
terminals.add('$')
print("Terminales: ", terminals)




first_set = compute_first(new_grammar, non_terminals, terminals)
follow_set = compute_follow(new_grammar, non_terminals, new_grammar[0][0], first_set)


print("FIRST sets:")
for non_terminal in non_terminals:
    print(f"FIRST({non_terminal}) = {first_set[non_terminal]}")


print("\nFOLLOW sets:")
for non_terminal in non_terminals:
    print(f"FOLLOW({non_terminal}) = {follow_set[non_terminal]}")

#eliminar la produccion s de la gramatica
new_grammar.pop(0)
gramatica = new_grammar
#agregarle el · al final de todas las producciones

new_grammar = punto(new_grammar)

# ---------------------TABLA SLR----------------------------
productions = indexGrammar(new_grammar)

# Construir las tablas SLR
action, goto, sr_conflicts, rr_conflicts = construir_tabla_SLR(automata, follow_set, terminals, non_terminals, productions)

# Verificar y manejar conflictos
if sr_conflicts or rr_conflicts:
    if sr_conflicts:
        print(f"Se encontraron conflictos shift/reduce en los siguientes estados y símbolos: {sr_conflicts}")
    if rr_conflicts:
        print(f"Se encontraron conflictos reduce/reduce en los siguientes estados y símbolos: {rr_conflicts}")
    raise SystemExit("Conflictos encontrados en la gramática. Deteniendo la ejecución.")


imprimir_tabla_SLR(action, goto)

gramatica = quitarPunto(gramatica)
productions2 = indexGrammar2(gramatica)



# ---------------------ANALIZADOR SINTACTICO----------------------------
# Ejemplo de uso
input_tokens = ['LPAREN', 'ID', 'RPAREN', 'TIMES', 'ID', 'PLUS', 'ID']
try:
    result = parse(input_tokens, action, goto, productions2)
    print(result)
except SyntaxError as e:
    print(e)