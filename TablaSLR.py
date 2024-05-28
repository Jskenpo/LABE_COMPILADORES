from collections import defaultdict

def compute_first(grammar, non_terminals, terminals):
    first = defaultdict(set)

    # Regla 1: Si X es un terminal, entonces FIRST(X) = {X}
    for terminal in terminals:
        first[terminal] = {terminal}

    # Regla 2 y 3: Calcular FIRST para los no terminales
    while True:
        updated = False
        for non_terminal in non_terminals:
            old_first = first[non_terminal].copy()
            for production in grammar:
                if production[0] == non_terminal:
                    first[non_terminal].update(first_of_production(first, production[1], terminals))
            if old_first != first[non_terminal]:
                updated = True
        if not updated:
            break

    return first

def first_of_production(first, production, terminals):
    result = set()
    for symbol in production:
        if symbol in terminals:
            result.add(symbol)
            break
        else:
            result.update(first[symbol])
            if '#' not in first[symbol]:
                break
    else:
        result.add('#')
    return result



def compute_follow(grammar, non_terminals, start_symbol, first):
    follow = defaultdict(set)
    follow[start_symbol] = {'$'}

    while True:
        updated = False
        for non_terminal in non_terminals:
            old_follow = follow[non_terminal].copy()
            for production in grammar:
                if non_terminal in production[1]:
                    for i, symbol in enumerate(production[1]):
                        if symbol == non_terminal:
                            if i + 1 < len(production[1]):
                                follow[non_terminal].update(first[production[1][i + 1]])
                                if '#' in first[production[1][i + 1]]:
                                    follow[non_terminal].update(follow[production[0]])
                                    follow[non_terminal].remove('#')
                            else:
                                follow[non_terminal].update(follow[production[0]])
            if old_follow != follow[non_terminal]:
                updated = True
        if not updated:
            break

    return follow




def construir_conjuntos_lr1(automata, gramatica, first_sets, follow_sets,no_terminales):
    conjuntos_lr1 = {}
    for estado in automata.states:
        conjunto_lr1 = defaultdict(set)
        for produccion in estado.productions:
            produccion_tupla = tuple(produccion)
            punto = produccion[1].index('·')
            if punto < len(produccion[1]):
                simbolo_siguiente = produccion[1][punto + 1]
                if simbolo_siguiente in no_terminales :
                    for terminal in first_sets[simbolo_siguiente]:
                        conjunto_lr1[(produccion_tupla, terminal)].add(produccion_tupla)
                    if '#' in first_sets[simbolo_siguiente]:
                        for terminal in follow_sets[produccion[0]]:
                            conjunto_lr1[(produccion_tupla, terminal)].add(produccion_tupla)
                else:
                    conjunto_lr1[(produccion_tupla, simbolo_siguiente)].add(produccion_tupla)
            else:
                for terminal in follow_sets[produccion[0]]:
                    conjunto_lr1[(produccion_tupla, terminal)].add(produccion_tupla)
        conjuntos_lr1[estado] = conjunto_lr1
    return conjuntos_lr1

def construir_tabla_slr(automata, gramatica, conjuntos_lr1):
    action_table = {}
    goto_table = {}
    for estado in automata.states:
        action_table[estado] = {}
        goto_table[estado] = {}
        for produccion, terminal in conjuntos_lr1[estado]:
            if produccion[1][-1] == '·':
                if terminal == '$' and produccion[0] == gramatica.inicial:
                    action_table[estado][terminal] = 'acc'
                else:
                    action_table[estado][terminal] = 'r' + str(gramatica.producciones.index(produccion))
            else:
                punto = produccion[1].index('·')
                simbolo_siguiente = produccion[1][punto + 1]
                if simbolo_siguiente in gramatica.terminales:
                    action_table[estado][simbolo_siguiente] = 'shift'
                else:
                    goto_table[estado][simbolo_siguiente] = siguiente_estado(automata, estado, simbolo_siguiente)
    return action_table, goto_table


def siguiente_estado(automata, estado_actual, simbolo):
    for transicion in automata.transitions:
        if transicion[0] == estado_actual and transicion[1] == simbolo:
            return transicion[2]
    return None